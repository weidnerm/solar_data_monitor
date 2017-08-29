until /usr/bin/python solar_monitor.py 2>>/home/pi/proj/solar/solar_data_monitor/solar_monitor_crash_log.txt; do
    CRASHTIME=`date`
    echo $CRASHTIME "solar_monitor.py crashed with exit code $?.  Respawning.." >> /home/pi/proj/solar/solar_data_monitor/solar_monitor_crash_log.txt
    sleep 10
done
