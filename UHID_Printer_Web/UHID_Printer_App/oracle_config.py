import cx_Oracle as oracle

# from oracle_config import *

ip = "172.20.200.16"

host = "khdb-scan.kdahit.com"

port = 1521

service_name = "newdb.kdahit.com"

instance_name = "NEWDB"

# ora_db = oracle.connect("appluser","appluser",dsn_tns)

# cursor = ora_db.cursor()


# host = 'khdb-scan'

# port = 1521

# service_name = "newdb.kdahit.com"

# instance_name = "NEWDB"

# dsn_tns = oracle.makedsn(ip,port,instance_name)

# ora_db = oracle.connect("ibaehis","ib123",dsn_tns)

# cursor = ora_db.cursor()


#   'oracle': {
#     'ENGINE': 'django.db.backends.oracle',
#     'NAME': 'NEWDB:1521/newdb.kdahit.com',
#     'NAME': ('(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=khdb-scan)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=newdb.kdahit.com)))'),
#     'USER': 'ibaehis',
#     'PASSWORD': 'ib123',


class Ora:
    def __init__(self):
        self.dsn_tns = oracle.makedsn(host, port, service_name=service_name)
        self.ora_db = oracle.connect("ibaehis", "ib123", self.dsn_tns)
        self.cursor = self.ora_db.cursor()

    def status_update(self):
        if self.ora_db:
            return "You have connected to the Database"

        else:
            return "Unable to connect to the database! Please contact the IT Department"

    # def __del__(self):
    # self.cursor.close()
    # self.ora_db.close()

    def get_patient_details(self, uhid):
        sql_qurey = """ select patient_id,patient_name,sex from mp_patient where patient_id= :uhid
        
        """

        self.cursor.execute(sql_qurey, [uhid])
        patient_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return patient_data

    def get_patient_details_for_label_ip(self, uhid):
        sql_qurey = """ 
        
        Select a.PATIENT_ID, a.PATIENT_NAME,decode(sex,'F','Female','M','Male','Unknown') Sex , 
        trunc((sysdate - a.DATE_OF_BIRTH) / 365, 0) || ' Y' as AGE, d.PRACTITIONER_NAME     
        from MP_Patient a join MP_PAT_Addresses b on b.PATIENT_ID = a.PATIENT_ID join IP_open_Encounter c on c.PATIENT_ID = a.PATIENT_ID  
        join AM_PRACTITIONER d on c.admit_practitioner_ID = d.PRACTITIONER_ID  
        WHERE  a.PATIENT_ID = :uhid
        
        """

        self.cursor.execute(sql_qurey, [uhid])
        patient_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return patient_data

    def get_patient_details_for_label_op(self, uhid):
        sql_qurey = """ 
        
        Select a.PATIENT_ID, a.PATIENT_NAME,decode(sex,'F','Female','M','Male','Unknown') Sex , 
        trunc((sysdate - a.DATE_OF_BIRTH) / 365, 0) || ' Y' as AGE, d.PRACTITIONER_NAME     
        from MP_Patient a join MP_PAT_Addresses b on b.PATIENT_ID = a.PATIENT_ID join op_current_patient c on c.PATIENT_ID = a.PATIENT_ID  
        join AM_PRACTITIONER d on c.practitioner_ID = d.PRACTITIONER_ID  
        WHERE  a.PATIENT_ID = :uhid 
        
        """

        self.cursor.execute(sql_qurey, [uhid])
        patient_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return patient_data

    def get_patient_details_for_label_both(self, uhid):
        sql_qurey = """ 
        
        Select a.PATIENT_ID, a.PATIENT_NAME,decode(sex,'F','Female','M','Male','Unknown') ||' '||c.patient_class GENDER, 
        trunc((sysdate - a.DATE_OF_BIRTH) / 365, 0) || ' Y' as AGE, d.PRACTITIONER_NAME ,c.visit_adm_date_time    
        from MP_Patient a join MP_PAT_Addresses b on b.PATIENT_ID = a.PATIENT_ID join pr_Encounter c on c.PATIENT_ID = a.PATIENT_ID  
        join AM_PRACTITIONER d on c.attend_practitioner_ID = d.PRACTITIONER_ID  WHERE  a.PATIENT_ID = :uhid
        
        """

        self.cursor.execute(sql_qurey, [uhid])
        patient_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return patient_data

    def get_patient_details_for_label_with_specimen(self, uhid):
        sql_qurey = """ 
        
        
        Select a.PATIENT_ID, a.PATIENT_NAME,decode(sex,'F','Female','M','Male','Unknown') Sex , 
        trunc((sysdate - a.DATE_OF_BIRTH) / 365, 0) || ' Y' as AGE,d.PRACTITIONER_NAME,f.DESC_ON_LABEL,i.PROCESS_DATE,i.SPECIMEN_NO,G.SHORT_DESC
        from MP_Patient a , AM_PRACTITIONER d , --BL_PATIENT_CHARGES_INTERFACE e --, \
        --OP_CURRENT_PATIENT c ,IP_OPEN_ENCOUNTER d, 
        RL_SPECIMEN_TYPE_CODE f, 
        RL_TEST_CODE g, RL_REQUEST_HEADER h, RL_REQUEST_DETAIL i   
        where a.PATIENT_ID = i.PATIENT_ID
        and  i.PATIENT_ID = h.PATIENT_ID
        and d.PRACTITIONER_ID = i.PERF_PHYSICIAN_ID
        and i.TEST_CODE = g.TEST_CODE
        and h.SPECIMEN_TYPE_CODE = f.SPECIMEN_TYPE_CODE
        and i.SPECIMEN_NO =h.SPECIMEN_NO
        AND a.PATIENT_ID = :uhid_get
        order by i.PROCESS_DATE desc
        ---and f.ADMIT_PRACTITIONER_ID = d.PRACTITIONER_ID
        --and e.BLNG_SERV_CODE like 'NMNM%' 
        
        """

        self.cursor.execute(sql_qurey, [uhid])
        patient_data = self.cursor.fetchall()

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return patient_data


if __name__ == "__main__":
    a = Ora()
    # b = a.get_online_consultation_report('01-Mar-2022','03-Apr-2022')
    b = a.get_package_contract_report("16-Jun-2018", "12-Jan-2022", "KH")

    print(b)

    for x in b:
        print(x)
