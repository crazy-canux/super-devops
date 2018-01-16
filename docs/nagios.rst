.. _nagios:

nagios
======

Services Status::

        0   OK
        1   Warning
        2   Critical
        3   Unknown

Nagios Output(just support 4kb data)::

        shortoutput - $SERVICEOUTPUT$
        -> The first line of text output from the last service check.
        perfdata - $SERVICEPERFDATA$
        -> Contain any performance data returned by the last service check.
        With format: | 'label'=value[UOM];[warn];[crit];[min];[max].
        longoutput - $LONGSERVICEOUTPUT$
        -> The full text output aside from the first line from the last service check.

        example:
        OK - shortoutput. |
        Longoutput line1
        Longoutput line2 |
        'perfdata'=value[UOM];[warn];[crit];[min];[max]

Threshold::

        warning  warn_min:warn_max
        critical crit_min:crit_max
        warn_min < warn_max <= crit_min < crit_max
        10 == 0:10     => <0 or >10 alert
        10: == 10:æ    => <10 alert
        ~:10 == -æ:10  => >10 alert
        10:20          => <10 or >20 alert
        @10:20         => >=10 or <= 20 alert
