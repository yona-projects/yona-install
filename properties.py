def db_settings(application_conf, setting):
    with open(str(application_conf.resolve()), 'r') as conf:
        content = conf.readlines()

        for line_no, line in enumerate(content.copy()):
            if line.startswith("# MariaDB"):
                del content[line_no:line_no + 3]

                content.insert(line_no, "db.default.driver = org.mariadb.jdbc.Driver")
                content.insert(line_no + 1, "jdbc:mariadb://{host}:{port}/{name}?useServerPrepStmts=true".format_map(setting))
                content.insert(line_no + 2, "db.default.user = {0}".format(setting['user']))
                content.insert(line_no + 3, "db.default.password = {0}".format(setting['passwd']))

        return content
