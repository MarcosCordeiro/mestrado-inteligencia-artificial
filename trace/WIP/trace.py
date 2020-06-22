import psutil, datetime, time, mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="changes",
    database="trace",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

def mysql_insert(process_id, process_name, user_name, exe_path, status, cpu_times, create_time):
    sql = "INSERT INTO trace_process(process_id, process_name, user_name, exe_path, status, cpu_times, create_time, log_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICA E KEY UPDA E process_id = "+ str(process_id) +", process_name = '"+ process_name + "', cpu_times=" + str(cpu_times) +"," + "create_time='" + str(create_time) + "', count_updates = count_updates + 1, status='" + status + "'"

    val = (process_id, process_name, user_name, exe_path, status, cpu_times, create_time, datetime.datetime.now())
    mycursor.execute(sql, val)

    mydb.commit()

    sql = "INSERT INTO trace_process_detail(process_id, process_name, user_name, exe_path, status, cpu_times, create_time, log_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    val = (process_id, process_name, user_name, exe_path, status, cpu_times, create_time, datetime.datetime.now())
    mycursor.execute(sql, val)

    mydb.commit()

def mysql_select():
    mycursor.execute("SELECT process_name FROM system_process WHERE operating_system = 'LNX';")
    return [item[0] for item in mycursor.fetchall()]

system_processes = mysql_select()

while(True):
    for proc in psutil.process_iter():
        try:
            processName = proc.name().strip()
            processID = proc.pid
            cpuTimes = sum(proc.cpu_times()[:2])
            createTime = datetime.datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S")
            status = proc.status().strip()
            exePath = proc.exe().strip()
            userName = proc.username().strip()
            
            if(not processName.startswith(tuple(system_processes))):
                print(processName , ' ::: ', processID, ' ::: ', cpuTimes, ' ::: ', createTime, ' ::: ', status, ' ::: ', exePath,' ::: ', userName)
                mysql_insert(processID, processName, userName, exePath, status, cpuTimes, createTime)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    time.sleep(5)