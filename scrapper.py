import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pickle

class Scrapper:
    def __init__(self,user_data_dir=None) -> None:
        self.is_loaded = False
        self.driver = None
        self.total_request_size = 0
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
                raise("Reached error page. Is mitmweb running?")
        except:
            pass

        # Apply filter to include only the requests with YouTube's user-agent in the headers. Also exclude all calls to stats for nerds.
        input_fields = self.driver.find_elements(By.TAG_NAME, 'input')
        input_fields[0].send_keys("~hq com.google.android.youtube") #!api/stats")
        input_fields[0].send_keys(Keys.ENTER)

        self.is_loaded = True
    
    def timestamp_to_epocs(self,timestamp: str):
        if(not timestamp):
            return None
        converted_timestamp = datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S.%f').timestamp()
        return converted_timestamp

    def extract_flow_id(self, url):
        return url.split('flows/')[1].split('/')[0]
    
    def append_epoch_timestamps(self, request_data):
        request_data['latency_metrics_epochs'] = {
            "client_connection_established": self.timestamp_to_epocs(request_data['latency_metrics']['client_connection_established'].split('(')[0] if request_data['latency_metrics']['client_connection_established'] else None),
            "server_connection_initiated": self.timestamp_to_epocs(request_data['latency_metrics']['server_connection_initiated'].split('(')[0] if request_data['latency_metrics']['server_connection_initiated'] else None),
            "server_tcp_handshake": self.timestamp_to_epocs(request_data['latency_metrics']['server_tcp_handshake'].split('(')[0] if request_data['latency_metrics']['server_tcp_handshake'] else None),
            "server_tls_handshake": self.timestamp_to_epocs(request_data['latency_metrics']['server_tls_handshake'].split('(')[0] if request_data['latency_metrics']['server_tls_handshake'] else None),
            "client_tls_handshake": self.timestamp_to_epocs(request_data['latency_metrics']['client_tls_handshake'].split('(')[0] if request_data['latency_metrics']['client_tls_handshake'] else None),
            "first_request_byte": self.timestamp_to_epocs(request_data['latency_metrics']['first_request_byte'] if request_data['latency_metrics']['first_request_byte'] else None),
            "request_complete": self.timestamp_to_epocs(request_data['latency_metrics']['request_complete'].split('(')[0] if(request_data['latency_metrics']['request_complete']) else None),
            "first_response_byte": self.timestamp_to_epocs(request_data['latency_metrics']['first_response_byte'].split('(')[0]) if request_data['latency_metrics']['first_response_byte'] else None,
            "response_complete": self.timestamp_to_epocs(request_data['latency_metrics']['response_complete'].split('(')[0]) if  request_data['latency_metrics']['response_complete'] else None,
            "client_connection_closed": self.timestamp_to_epocs(request_data['latency_metrics']['client_connection_closed'].split('(')[0] if request_data['latency_metrics']['client_connection_closed'] else None),
            "server_connection_closed": self.timestamp_to_epocs(request_data['latency_metrics']['server_connection_closed'].split('(')[0] if request_data['latency_metrics']['server_connection_closed'] else None),
        }

    def extract_trace_data(self):
        mapping = {
            'Client conn. established:': "client_connection_established",
            'Server conn. initiated:': "server_connection_initiated",
            'Server conn. TCP handshake:': "server_tcp_handshake",
            'Server conn. TLS handshake:': "server_tls_handshake",
            'Client conn. TLS handshake:': "client_tls_handshake",
            'First request byte:': "first_request_byte",
            'Request complete:': "request_complete",
            'First response byte:': "first_response_byte",
            'Response complete:': "response_complete",
            'Server conn. closed:': "server_connection_closed",
            'Client conn. closed:': "client_connection_closed"
        }

        if(not self.is_loaded):
            self.launch_mitm()

        # Wait for the trace to be loaded before proceeding
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tr"))
        )
        

        # Chrome is currently not loading all the traces into DOM, they load up as we scroll down. Find a way around this. scrolling the request view isnt working
        # So it turns out, mitm only loads the rows that fit the window and replaces them as we scroll. Possibly for perfomrance reasons. So we need to deal with that
        # one way is by sending down key, and see if the flows have changed.
        
        
        flow_table = self.driver.find_elements(By.CLASS_NAME,"flow-table")[0]
        
        table_body = flow_table.find_elements(By.TAG_NAME,"tbody")[0]
        flows = table_body.find_elements(By.TAG_NAME,"tr")

        body = self.driver.find_element(By.TAG_NAME, 'Body')

        # this is the number of flows we get on the page at a given time
        last_index = len(flows) - 2
        if(os.path.exists('./mitm_data.pkl')):
            with open('./mitm_data.pkl','rb') as pkl_file:
                extracted_data = pickle.load(pkl_file)
        else:
            extracted_data = {}

        for index,flow in enumerate(flows):
            sub_elements = flow.find_elements(By.TAG_NAME,"td")
            if(not len(sub_elements)):
                continue
            
            flow.click()
            flow_id = self.extract_flow_id(self.driver.current_url)
            
            if(flow_id in extracted_data):
                size = extracted_data[flow_id]["size_bytes"]
                self.total_request_size += size
                continue
            
            # Click the "timing" column
            self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/nav/a[4]").click()

            # Extract URL
            request_data = {
                "url": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[3]".format(index+1)).text,
                "method": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[4]".format(index+1)).text,
                "size": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[6]".format(index+1)).text,
                "time": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[7]".format(index+1)).text,
                "latency_metrics": dict.fromkeys(mapping.values())
            }

            request_size = request_data['size']
            if(request_size and type(request_size) == type("")):
                if('kb' in request_size):
                    size = float(request_size.split('kb')[0]) * 1024
                elif('mb' in request_size):
                    size = float(request_size.split('mb')[0]) * 1024 * 1024
                elif('b' in request_size):
                    size = float(request_size.split('b')[0])
                else:
                    size = int(request_size)
            else:
                size = 0
            
            self.total_request_size += size
            request_data["size_bytes"] = size

            # Get the table body
            timing_table = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/section/table/tbody")
            timing_table_elements = timing_table.find_elements(By.TAG_NAME,"tr")
            for element in timing_table_elements:
                entries = element.find_elements(By.TAG_NAME, 'td')
                key = mapping[entries[0].text]
                request_data["latency_metrics"][key] = entries[1].text.split('(')[0]

            self.append_epoch_timestamps(request_data)

            extracted_data[flow_id] = request_data


        while(True):
            body.send_keys(Keys.DOWN)
            updated_data= table_body.find_elements(By.TAG_NAME,"tr")
            new_elements = list(set(updated_data).difference(set(flows)))
            if(len(new_elements) == 0):
                break
            # we should only have one element in the new_elements array - but for some reasone, we get 2.
            for new_element in new_elements:
                new_element.click()

                flow_id = self.extract_flow_id(self.driver.current_url)
                if(flow_id in extracted_data):
                    size = extracted_data[flow_id]["size_bytes"]
                    self.total_request_size += size
                    continue

                # Click the "timing" column. Sometimes there is an additonal "error" column. Handle that too.
                timing_column = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/nav/a[4]") 
                if(timing_column.text != 'Timing'):
                    timing_column = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/nav/a[5]")
                timing_column.click()
                request_data = {
                    "url": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[3]".format(last_index)).text,
                    "method": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[4]".format(last_index)).text,
                    "size": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[6]".format(last_index)).text,
                    "time": self.driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div[1]/table/tbody/tr[{}]/td[7]".format(last_index)).text,
                    "latency_metrics": dict.fromkeys(mapping.values())
                }
                request_size = request_data['size']
                if(request_size and type(request_size) == type("")):
                    if('kb' in request_size):
                        size = float(request_size.split('kb')[0]) * 1024
                    elif('mb' in request_size):
                        size = float(request_size.split('mb')[0]) * 1024 * 1024
                    elif('b' in request_size):
                        size = float(request_size.split('b')[0])
                    else:
                        size = int(request_size)
                else:
                    size = 0
                
                self.total_request_size += size
                request_data["size_bytes"] = size

                # Get the table body
                timing_table = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/section/table/tbody")
                timing_table_elements = timing_table.find_elements(By.TAG_NAME,"tr")
                for element in timing_table_elements:
                    entries = element.find_elements(By.TAG_NAME, 'td')
                    key = mapping[entries[0].text]
                    request_data["latency_metrics"][key] = entries[1].text.split('(')[0]
                
                self.append_epoch_timestamps(request_data)
                extracted_data[flow_id] = request_data
            flows = updated_data
        
        print(len(extracted_data.keys()))

        with open('mitm_data.pkl','wb') as handle:
            pickle.dump(extracted_data,handle)
        with open('./trace_size.csv','r') as csv_handle:
            trace = sum(1 for _ in csv_handle)
        
        with open('./trace_size.csv','a+') as csv_handle:
            if(trace == 0):
                csv_handle.write("flow_number, size\n")
                trace += 1
            csv_handle.write("{},{}mb\n".format(trace, round(self.total_request_size/1024/1024,3)))
        print(self.total_request_size)
        self.driver.quit()

    def __del__(self):
        self.driver.quit()


scrapper = Scrapper()
scrapper.extract_trace_data()


        