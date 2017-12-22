update policy set filetype_limit='pe_x32,pe_x64,msi_x32,msi_x64,archive,office,pdf,unknown,script,apk' where method_name='SMASH'
go
insert configuration values('auto_reanalyze','{"enabled":false,"afterdays":3}')
go
UPDATE configuration SET value = '44' where key_name = 'version'