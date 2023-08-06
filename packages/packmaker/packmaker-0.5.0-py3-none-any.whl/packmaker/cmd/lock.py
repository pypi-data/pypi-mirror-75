# vim:set ts=4 sw=4 et nowrap syntax=python ff=unix:
#
# Copyright 2019 Mark Crewson <mark@crewson.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import dateutil.parser
import json

from ..curse.curseforge import Curseforge
from ..framew.application import OperationError
from ..framew.cmdapplication import Subcommand
from ..framew.config import ConfigError
from ..framew.log import getlog
from ..packdef import PackDefinition, ModDefinition

##############################################################################

depend_types = ["_all_", "embeddedlib", "optional", "required", "tool", "incompatible", "include"]


class LockCommand (Subcommand):
    """
    Lock the modpack. Find mod download urls, generate a packmaker.lock file.
    """

    name = 'lock'

    default_packmaker_yml = 'packmaker.yml'

    def get_cmdline_parser(self):
        parser = super(LockCommand, self).get_cmdline_parser()
        parser.add_argument('packdef',
                            nargs='*',
                            default=[LockCommand.default_packmaker_yml],
                            help='modpack definition file')
        return parser

    def setup(self):
        super(LockCommand, self).setup()
        self.log = getlog()

    def setup_command(self, arguments):
        self.setup_api()
        self.setup_db()

    def setup_api(self):
        authn_token = self.config.get('curseforge::authentication_token')
        if authn_token is None:
            raise ConfigError('No curseforge authentication token')
        self.api = Curseforge(authn_token)

    def setup_db(self):
        db_filename = self.config.get('curseforge::moddb_filename')
        if db_filename is None:
            raise ConfigError('No moddb_filename parameter in configuration')

        self.log.moreinfo('Loading curseforge database ...')
        with open(db_filename, 'r') as cf:
            self.db = json.load(cf)

    def run_command(self, parsed_args):

        self.log.info('Reading pack definition ...')
        pack = PackDefinition(parsed_args.packdef)
        pack.load()

        # warn if the main metadata fields are not defined in the packdef
        for m in ('name', 'title', 'version', 'authors', 'minecraft_version'):
            val = getattr(pack, m)
            if val is None or val == []:
                self.log.warn('No \'{}\' field defined in {}'.format(m, ', '.join(parsed_args.packdef)))

        packlock = pack.get_packlock()
        packlock.set_all_metadata(pack)

        self.mc_version = pack.minecraft_version

        self.modloader = None
        if pack.forge_version is not None:
            self.modloader = 'forge'

        self.log.info('Resolving mods...')
        self.mod_definitions = pack.get_all_mods()
        self.resolve_mods(packlock)

        self.log.info('Resolving resourcepacks...')
        self.resourcepack_definitions = pack.get_all_resourcepacks()
        self.resolve_resourcepacks(packlock)

        self.log.info('Adding files...')
        for filesdef in pack.files:
            packlock.add_files(filesdef)

        self.log.info('Adding extra options (if any)...')
        if pack.routhio is not None:
            packlock.add_extraopt('routhio', pack.routhio)

        self.log.info('Writing pack lock...')
        packlock.save()

        self.log.moreinfo('Done.')

    def resolve_mods(self, packlock):
        for moddef in self.mod_definitions:
            self.resolve_one_mod(moddef, packlock)

    def resolve_one_mod(self, moddef, packlock):
        self.log.info('Resolving: {}'.format(moddef.slug))
        modslug, modname, modid, modauthor, modwebsite = self.find_addon_by_slug(moddef.slug, 'mod')
        modfile_found = self.find_addon_file(modid, moddef.version)
        if modfile_found is None:
            raise OperationError('Cannot find a mod file for {}'.format(moddef.slug))

        packlock.add_resolved_mod(moddef, {'projectId': modid,
                                           'name': modname,
                                           'author': modauthor,
                                           'website': modwebsite,
                                           'fileId': modfile_found['id'],
                                           'fileName': modfile_found['fileName'],
                                           'downloadUrl': modfile_found['downloadUrl']
                                           })

        self.check_mod_dependencies(modfile_found['dependencies'], moddef.ignoredeps, packlock)

    def check_mod_dependencies(self, dependencies, ignoredeps, packlock):
        self.log.moreinfo("Checking for dependencies...")
        if type(ignoredeps) is str and ignoredeps == "all":
            self.log.moreinfo('  all dependencies ignored ("ingoreddeps: all")')
            return
        if len(dependencies) == 0:
            self.log.moreinfo('  no dependencies')
            return

        for depmod in dependencies:
            modid = depmod['addonId']
            deptype = depmod['type']
            if deptype != 3:
                self.log.moreinfo('  ignoring dependency (id={}, type={} ({}))'.format(modid, deptype, depend_types[deptype]))
                continue

            depslug, depname, depid, depauthors, depwebsite = self.find_addon_by_id(modid, 'mod')
            if depslug in ignoredeps:
                self.log.info('  Ignoring dependency: {}'.format(depslug))
                continue

            self.log.info('  Solving dependency: {}'.format(depslug))
            try:
                # search the packdef. is this mod already included?
                packlock.get_mod(depslug)
                self.log.info('  Dependent mod already resolved')
            except KeyError:
                # Not already included. Is it an already solved dependency?
                for depdef in self.mod_definitions:
                    if depdef.slug == depslug:
                        self.log.info('  Dependent mod already include in packdef')
                        break
                # Not included and not already solved: resolve this dependent mod
                else:
                    self.log.info('  Mod needs resolution: {}'.format(depslug))
                    self.resolve_one_mod(ModDefinition(depslug, None), packlock)

    def resolve_resourcepacks(self, packlock):
        for repdef in self.resourcepack_definitions:
            repslug, repname, repid, repauthor, repwebsite = self.find_addon_by_slug(repdef.slug, 'resourcepack')
            repfile_found = self.find_addon_file(repid, repdef.version)
            if repfile_found is None:
                raise OperationError('Cannot find a resourcepack file for {}'.format(repdef.slug))

            packlock.add_resolved_resourcepack(repdef, {'projectId': repid,
                                                        'name': repname,
                                                        'author': repauthor,
                                                        'website': repwebsite,
                                                        'fileId': repfile_found['id'],
                                                        'fileName': repfile_found['fileName'],
                                                        'downloadUrl': repfile_found['downloadUrl']
                                                        })

    def find_addon_by_slug(self, slug, category):
        if slug in self.db and self.db[slug]['category'] == category:
            return slug, \
                self.db[slug]['name'], \
                self.db[slug]['id'], \
                self.db[slug]['authors'][0]['name'], \
                self.db[slug]['websiteUrl']
        else:
            return self.manual_addon_search(slug, category)

    def find_addon_by_id(self, id, category):
        for slug, entry in self.db.items():
            if entry['id'] == id and entry['category'] == category:
                return entry['slug'], \
                    entry['name'], \
                    id, \
                    entry['authors'][0]['name'], \
                    entry['websiteUrl']
        else:
            addon = self.api.get_addon(id)
            return addon['slug'], \
                addon['name'], \
                addon['id'], \
                addon['authors'][0]['name'], \
                addon['websiteUrl']

    def manual_addon_search(self, slug, category):
        self.log.warn('Cannot find addon in local db: {}. Manually searching...'.format(slug))

        if category == 'mod':
            sectionid = 6
        elif category == 'resourcepack':
            sectionid = 12
        else:
            raise Exception('unknown category passed to manual_addon_search()')

        searchresults = list(({'name': addon['name'], 'id': addon['id'], 'slug': addon['slug'],
                               'authors': addon['authors'], 'websiteUrl': addon['websiteUrl']}
                              for addon in self.api.yield_addons_by_criteria(gameId=432, sectionId=sectionid,
                                                                             gameVersions=self.mc_version,
                                                                             searchFilter=slug)))

        if len(searchresults) < 1:
            raise OperationError('Cannot find an addon named \'{}\''.format(slug))
        elif len(searchresults) > 1:
            self.log.warn('Multiple search results found ({}).  Looking for an exact match in results...'
                          .format(len(searchresults)))
            for sresult in searchresults:
                if sresult['slug'] == slug:
                    searchresult = sresult
                    self.log.warn('Found it! ... {} (id = {})'.format(searchresult['slug'], searchresult['id']))
                    break
            else:
                searchresult = searchresults[0]
                self.log.warn('No exact match found! Using the first one (this could be wildly wrong) ... {} (id = {})'
                              .format(searchresult['slug'], searchresult['id']))
        else:
            searchresult = searchresults[0]
            self.log.warn('Found it! ... {} (id = {})'.format(searchresult['slug'], searchresult['id']))

        return (searchresult['slug'], searchresult['name'], searchresult['id'],
                searchresult['authors'][0]['name'], searchresult['websiteUrl'])

    def find_addon_file(self, id, required_version):
        latestTimestamp = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
        addon_found = None
        for addonfile in self.api.get_addon_files(id):

            if required_version != 'latest':
                # exact version specifed.  Just use it, with no additonal checks
                if addonfile['fileName'] == required_version or \
                   addonfile['displayName'] == required_version:
                    return addonfile

            else:
                if self.mc_version not in addonfile['gameVersion']:
                    continue

                if self.modloader == 'forge' and 'Fabric' in addonfile['gameVersion']:
                    continue
                elif self.modloader == 'fabric' and 'Forge' in addonfile['gameVersion']:
                    continue

                timestamp = dateutil.parser.parse(addonfile['fileDate'])
                if timestamp > latestTimestamp:
                    addon_found = addonfile
                    latestTimestamp = timestamp

        return addon_found

##############################################################################
# THE END
