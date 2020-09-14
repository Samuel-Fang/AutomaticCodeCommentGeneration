def camera_snapshot(self, camera_id, **kwargs):
        api = self._api_info['camera']
        payload = dict({
            '_sid': self._sid,
            'api': api['name'],
            'method': 'GetSnapshot',
            'version': api['version'],
            'cameraId': camera_id,
        }, **kwargs)
        response = self._get(api['url'], payload)

        return response.content
#-----------------------------------------------------------------------------------------------------
def parse_pattern(pattern):
    if isinstance(pattern, NumberPattern):
        return pattern

    def _match_number(pattern):
        rv = number_re.search(pattern)
        if rv is None:
            raise ValueError('Invalid number pattern %r' % pattern)
        return rv.groups()

    pos_pattern = pattern

    # Do we have a negative subpattern?
    if ';' in pattern:
        pos_pattern, neg_pattern = pattern.split(';', 1)
        pos_prefix, number, pos_suffix = _match_number(pos_pattern)
        neg_prefix, _, neg_suffix = _match_number(neg_pattern)
    else:
        pos_prefix, number, pos_suffix = _match_number(pos_pattern)
        neg_prefix = '-' + pos_prefix
        neg_suffix = pos_suffix
    if 'E' in number:
        number, exp = number.split('E', 1)
    else:
        exp = None
    if '@' in number:
        if '.' in number and '0' in number:
            raise ValueError('Significant digit patterns can not contain '
                             '"@" or "0"')
    if '.' in number:
        integer, fraction = number.rsplit('.', 1)
    else:
        integer = number
        fraction = ''

    def parse_precision(p):
        """Calculate the min and max allowed digits"""
        min = max = 0
        for c in p:
            if c in '@0':
                min += 1
                max += 1
            elif c == '#':
                max += 1
            elif c == ',':
                continue
            else:
                break
        return min, max

    int_prec = parse_precision(integer)
    frac_prec = parse_precision(fraction)
    if exp:
        exp_plus = exp.startswith('+')
        exp = exp.lstrip('+')
        exp_prec = parse_precision(exp)
    else:
        exp_plus = None
        exp_prec = None
    grouping = babel.numbers.parse_grouping(integer)
    return NumberPattern(pattern, (pos_prefix, neg_prefix),
                         (pos_suffix, neg_suffix), grouping,
                         int_prec, frac_prec,
                         exp_prec, exp_plus)
#-----------------------------------------------------------------------------------------------------
def init_connector(self):
        self.using_ssh = bool(self.sshkey or self.sshserver)

        if self.sshkey and not self.sshserver:
            # We are using ssh directly to the controller, tunneling localhost to localhost
            self.sshserver = self.url.split('://')[1].split(':')[0]

        if self.using_ssh:
            if tunnel.try_passwordless_ssh(self.sshserver, self.sshkey, self.paramiko):
                password=False
            else:
                password = getpass("SSH Password for %s: "%self.sshserver)
        else:
            password = False

        def connect(s, url):
            url = disambiguate_url(url, self.location)
            if self.using_ssh:
                self.log.debug("Tunneling connection to %s via %s"%(url, self.sshserver))
                return tunnel.tunnel_connection(s, url, self.sshserver,
                            keyfile=self.sshkey, paramiko=self.paramiko,
                            password=password,
                )
            else:
                return s.connect(url)

        def maybe_tunnel(url):
            url = disambiguate_url(url, self.location)
            if self.using_ssh:
                self.log.debug("Tunneling connection to %s via %s"%(url, self.sshserver))
                url,tunnelobj = tunnel.open_tunnel(url, self.sshserver,
                            keyfile=self.sshkey, paramiko=self.paramiko,
                            password=password,
                )
            return url
        return connect, maybe_tunnel
#-----------------------------------------------------------------------------------------------------
def sign(self, value):
        value = want_bytes(value)
        timestamp = base64_encode(int_to_bytes(self.get_timestamp()))
        sep = want_bytes(self.sep)
        value = value + sep + timestamp
        return value + sep + self.get_signature(value)
#-----------------------------------------------------------------------------------------------------
def initialize_subcommand(self, subc, argv=None):
        subapp,help = self.subcommands.get(subc)

        if isinstance(subapp, basestring):
            subapp = import_item(subapp)

        # clear existing instances
        self.__class__.clear_instance()
        # instantiate
        self.subapp = subapp.instance()
        # and initialize subapp
        self.subapp.initialize(argv)
#-----------------------------------------------------------------------------------------------------
def mk_constant(cnst_syc):
    s_dt = one(cnst_syc).S_DT[1500]()
    cnst_lsc = one(cnst_syc).CNST_LFSC[1502].CNST_LSC[1503]()
    
    if s_dt.Name == 'boolean':
        return cnst_lsc.Value.lower() == 'true'
    
    if s_dt.Name == 'integer':
        return int(cnst_lsc.Value)
    
    if s_dt.Name == 'real':
        return float(cnst_lsc.Value)
    
    if s_dt.Name == 'string':
        return str(cnst_lsc.Value)
#-----------------------------------------------------------------------------------------------------
def pdf_case_report(institute_id, case_name):

    institute_obj, case_obj = institute_and_case(store, institute_id, case_name)
    data = controllers.case_report_content(store, institute_obj, case_obj)

    # add coverage report on the bottom of this report
    if current_app.config.get('SQLALCHEMY_DATABASE_URI'):
        data['coverage_report'] = controllers.coverage_report_contents(store, institute_obj, case_obj, request.url_root)

    # workaround to be able to print the case pedigree to pdf
    if case_obj.get('madeline_info') is not None:
        with open(os.path.join(cases_bp.static_folder, 'madeline.svg'), 'w') as temp_madeline:
            temp_madeline.write(case_obj['madeline_info'])

    html_report = render_template('cases/case_report.html', institute=institute_obj, case=case_obj, format='pdf', **data)
    return render_pdf(HTML(string=html_report), download_filename=case_obj['display_name']+'_'+datetime.datetime.now().strftime("%Y-%m-%d")+'_scout.pdf')
#-----------------------------------------------------------------------------------------------------
def backup(self):

        if PyFunceble.CONFIGURATION["auto_continue"]:
            # The auto_continue subsystem is activated.

            # We initiate the location where we are going to save the data to backup.
            data_to_backup = {}
            # We get the current counter states.
            configuration_counter = PyFunceble.INTERN["counter"]["number"]

            # We initiate the data we have to backup.
            data_to_backup[PyFunceble.INTERN["file_to_test"]] = {
                # We backup the number of tested.
                "tested": configuration_counter["tested"],
                # We backup the number of up.
                "up": configuration_counter["up"],
                # We backup the number of down.
                "down": configuration_counter["down"],
                # We backup the number of invalid.
                "invalid": configuration_counter["invalid"],
            }

            # We initiate the final data we have to save.
            # We initiate this variable instead of updating backup_content because
            # we do not want to touch the backup_content.
            to_save = {}

            # We add the backup_content into to_save.
            to_save.update(self.backup_content)
            # And we overwrite with the newly data to backup.
            to_save.update(data_to_backup)

            # Finaly, we save our informations into the log file.
            Dict(to_save).to_json(self.autocontinue_log_file)
#-----------------------------------------------------------------------------------------------------
def _add_run_info(self, idx, name='', timestamp=42.0, finish_timestamp=1.337,
                      runtime='forever and ever', time='>>Maybe time`s gone on strike',
                      completed=0, parameter_summary='Not yet my friend!',
                      short_environment_hexsha='N/A'):

        if idx in self._single_run_ids:
            # Delete old entries, they might be replaced by a new name
            old_name = self._single_run_ids[idx]
            del self._single_run_ids[old_name]
            del self._single_run_ids[idx]
            del self._run_information[old_name]

        if name == '':
            name = self.f_wildcard('$', idx)
        # The `_single_run_ids` dict is bidirectional and maps indices to run names and vice versa
        self._single_run_ids[name] = idx
        self._single_run_ids[idx] = name

        info_dict = {'idx': idx,
                     'timestamp': timestamp,
                     'finish_timestamp': finish_timestamp,
                     'runtime': runtime,
                     'time': time,
                     'completed': completed,
                     'name': name,
                     'parameter_summary': parameter_summary,
                     'short_environment_hexsha': short_environment_hexsha}

        self._run_information[name] = info_dict
        self._length = len(self._run_information)
#-----------------------------------------------------------------------------------------------------
def remove_ancestors_of(self, node):
        if isinstance(node, int):
            warnings.warn('Calling remove_ancestors_of() with a node id is deprecated,'
                          ' use a DAGNode instead',
                          DeprecationWarning, 2)
            node = self._id_to_node[node]

        anc = nx.ancestors(self._multi_graph, node)
        # TODO: probably better to do all at once using
        # multi_graph.remove_nodes_from; same for related functions ...
        for anc_node in anc:
            if anc_node.type == "op":
                self.remove_op_node(anc_node)