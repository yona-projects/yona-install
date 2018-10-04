def db_settings(application_conf, setting):
    db_url = "db.default.url = \"jdbc:mariadb://{host}:{port}/{name}?useServerPrepStmts=true\"\n"

    with open(str(application_conf.resolve()), 'r') as conf:
        content = conf.readlines()

        for line_no, line in enumerate(content.copy()):
            if line.startswith("# MariaDB"):
                del content[line_no + 1:line_no + 5]

                content.insert(line_no + 1, "db.default.driver = org.mariadb.jdbc.Driver\n")
                content.insert(line_no + 2, db_url.format_map(setting))
                content.insert(line_no + 3, "db.default.user = {0}\n".format(setting['user']))
                content.insert(line_no + 4, "db.default.password = {0}\n".format(setting['passwd']))

        return content
