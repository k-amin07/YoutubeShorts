import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

class Scrapper:
    def __init__(self,user_data_dir=None) -> None:
        self.is_loaded = False
        self.driver = None
        if(user_data_dir):
            self.user_data_dir = user_data_dir
        else:
            self.user_data_dir = "/var/tmp/chrome_mitm/"
        
        if(not os.path.exists(self.user_data_dir)):
            os.makedirs(self.user_data_dir)
    
    def configure_driver(self):
        chrome_driver_service = Service(ChromeDriverManager().install())
        dir_arg = '--user-data-dir=' + self.user_data_dir
        options = Options()
        options.add_argument(dir_arg)
        options.add_argument('--start-maximized')
        try:
            self.driver = webdriver.Chrome(service=chrome_driver_service, options=options)
        except Exception as e:
            if('user data directory' in str(e)):
                raise("Data directory already in use, please choose a different one")
            else:
                raise str(e)
    
    def launch_mitm(self):
        if(not self.driver):
            self.configure_driver()
        
        errorpage = None
        self.driver.get("http://localhost:8081/#/flows")
        
        try:
            errorpage = self.driver.find_element(By.CLASS_NAME,'neterror')
            if(errorpage):
                raise("Reached error page. Is mitmweb rnning?")
        except:
            pass
        self.is_loaded = True
    
    def timestamp_to_epocs(self,timestamp: str):
        converted_timestamp = datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S.%f').timestamp()
        return converted_timestamp
    
    def append_epoch_timestamps(self, request_data):
        request_data['latency_metrics_epochs'] = {
            "client_connection_established": self.timestamp_to_epocs(request_data['latency_metrics']['client_connection_established'].split('(')[0]),
            "server_connection_initiated": self.timestamp_to_epocs(request_data['latency_metrics']['server_connection_initiated'].split('(')[0]),
            "server_tcp_handshake": self.timestamp_to_epocs(request_data['latency_metrics']['server_tcp_handshake'].split('(')[0]),
            "server_tls_handshake": self.timestamp_to_epocs(request_data['latency_metrics']['server_tls_handshake'].split('(')[0]),
            "client_tls_handshake": self.timestamp_to_epocs(request_data['latency_metrics']['client_tls_handshake'].split('(')[0]),
            "first_request_byte": self.timestamp_to_epocs(request_data['latency_metrics']['first_request_byte']),
            "request_complete": self.timestamp_to_epocs(request_data['latency_metrics']['request_complete'].split('(')[0]),
            "first_response_byte": self.timestamp_to_epocs(request_data['latency_metrics']['first_response_byte'].split('(')[0]),
            "response_complete": self.timestamp_to_epocs(request_data['latency_metrics']['response_complete'].split('(')[0]),
            "client_connection_closed": self.timestamp_to_epocs(request_data['latency_metrics']['client_connection_closed'].split('(')[0]),
            "server_connection_closed": self.timestamp_to_epocs(request_data['latency_metrics']['server_connection_closed'].split('(')[0]),
        }

    def extract_trace_data(self):
        columns = ['Request', 'Response','Connection','Timing']
        if(not self.is_loaded):
            self.launch_mitm()

        # Wait for the trace to be loaded before proceeding
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )


        # Chrome is currently not loading all the traces into DOM, they load up as we scroll down. Find a way around this. scrolling the request view isnt working
        self.driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", self.driver.find_element(By.CLASS_NAME,'flow-table'))
        self.driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", self.driver.find_element(By.CLASS_NAME,'flow-table'))
        self.driver.execute_script("arguments[0].scroll(0, 0);", self.driver.find_element(By.CLASS_NAME,'flow-table'))
        
        flow_table = self.driver.find_elements(By.CLASS_NAME,"flow-table")[0]
        table_body = flow_table.find_elements(By.TAG_NAME,"tbody")[0]
        flows = table_body.find_elements(By.TAG_NAME,"tr")

        extracted_data = []
        for index,flow in enumerate(flows):
            sub_elements = flow.find_elements(By.TAG_NAME,"td")
            if(not len(sub_elements)):
                continue
            
            flow.click()
            
            # Click the "timing" column
            self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/nav/a[4]").click()
            # Extract URL
            request_data = {
                "url": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[3]".format(index+1)).text,
                "method": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[4]".format(index+1)).text,
                "size": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[6]".format(index+1)).text,
                "time": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[7]".format(index+1)).text,
                "latency_metrics": {
                    # All of the following XPaths are static and do not change across requests.
                    "client_connection_established": self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[1]/td[2]").text,
                    "server_connection_initiated": self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[2]/td[2]").text,
                    "server_tcp_handshake": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[3]/td[2]").text,
                    "server_tls_handshake": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[4]/td[2]").text,
                    "client_tls_handshake": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[5]/td[2]").text,
                    "first_request_byte": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[6]/td[2]").text,
                    "request_complete": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[7]/td[2]").text,
                    "first_response_byte": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[8]/td[2]").text,
                    "response_complete": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[9]/td[2]").text,
                    "client_connection_closed": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[10]/td[2]").text,
                    "server_connection_closed": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[3]/section/table/tbody/tr[11]/td[2]").text
                }
            }

            self.append_epoch_timestamps(request_data)

            extracted_data.append(request_data)

        print(extracted_data)

    def __del__(self):
        self.driver.quit()


scrapper = Scrapper()
scrapper.extract_trace_data()


        