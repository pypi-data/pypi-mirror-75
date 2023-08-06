#
# service: Caller: implement rest/swagger caller functionality
#
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4:
# 
#
import logging
import os
import json
import csv
import behavioral_signals_swagger_client as swagger_client
import time
from behavioral_signals_cli.frames_csv import frames_to_csv

class Caller():
    def __init__(self,opts,polling_time=5,indent=1):
        self.indent = indent
        self.opts = opts
        self.api = swagger_client.DefaultApi()
        self.api.api_client.configuration.host = opts.apiurl
        self.api.api_client.configuration.api_key['X-Auth-Token'] =\
            opts.apitoken
        self.polling_time = polling_time

    # -- obtain process info and poll if necessary
    def GetInfo(self, pid, poll=False):
        elapsed_time = 0
        wait,resp = self.getInfo(pid)
        if not poll:
            return resp
        while wait:
            time.sleep(self.polling_time)
            elapsed_time += self.polling_time
            wait,resp = self.getInfo(pid)

        if elapsed_time > 0 :
            logging.info("{} : polled process for {} seconds".
                format(pid,elapsed_time))

        return resp

    # -- obtain process results and dump them to a file
    def GetResults(self,pid,output_dir=None,dest=None):
        results = {}
        try:
            results = self.api.get_process_results(self.opts.apiid, pid)
            results = results.to_dict()
        except ValueError as e:
            if str(e) == "Invalid value for `basic`, must not be `None`":
                logging.warning("{}: No process results output".format(pid))
            else:
                logging.warning("{}: Process failed: {}".format(pid,e))
                results=None
        except Exception as e:
            if e.status == 405 or e.status == 503:
                msg = self.getResponse(e.body, 'message')
                logging.warning("{}: Process Results failure: {}/{}".format(
                    pid, msg, e.status))
                results=None
            else:
                raise
        finally:
            if results is not None:
                self.saveOutput2File(results, output_dir, dest, pid=pid)
        return results

    # -- obtain frame results and dump them to a file
    def GetFrameResults(self,pid,output_dir=None,dest=None):
        results = {}
        try:
            results = self.api.get_process_results_frames(self.opts.apiid, pid)
            results = results.to_dict()
        except ValueError as e:
            if str(e) == "Invalid value for `frames`, must not be `None`":
                logging.warning("{}: No frames results output".format(pid))
            else:
                logging.warning("{}: Process failed: {}".format(pid,e))
                results=None
        except Exception as e:
            if e.status == 405 or e.status == 503:
                msg = self.getResponse(e.body, 'message')
                logging.warning("{}: Frame Results failure: {}/{}".format(
                    pid, msg, e.status))
                results=None
            else:
                raise
        finally:
            if results is not None:
                self.saveOutput2File(results, output_dir, dest, "_frames", pid=pid)
        return results

    # -- obtain ASR results from caller
    # -- handle some exceptions -- return empty list
    def GetASRResults(self,pid,output_dir=None,dest=None):
        results = {}
        try:
            results = self.api.get_process_results_asr(self.opts.apiid, pid)
            results = results.to_dict()
            if results.get("predictions") == None:
                results.pop("predictions", None)
        except ValueError as e:
            # -- in case there is no ASR record for it
            if str(e) == "Invalid value for `words`, must not be `None`":
                logging.warning("{}: No ASR output".format(pid))
            else:
                logging.warning("{}: ASR failed: {}".format(pid,e))
                results=None
        except Exception as e:
            if e.status == 405 or e.status == 503:
                msg = self.getResponse(e.body, 'message')
                logging.warning("{}: ASR failure: {}/{}".format(
                    pid, msg, e.status))
                results=None
            else:
                raise
        finally:
            if results is not None:
                self.saveOutput2File(results, output_dir, dest, "_words", pid=pid)
        return results
    # ----------------------------------------------------------------------
    # -- obtain process info -- see if we should continue to wait
    def getInfo(self,pid):
        resp = self.api.get_process_info(self.opts.apiid,pid)
        if resp.status == -1:
            logging.info("{}: transient error -- retrying".format(pid))
            return False,resp
        
        if resp.status in [0,1]:
            return True,resp
        return False,resp

    # -- save output to file
    def saveOutput2File(self, results, output_dir, dest, suffix="", pid=0):
        if not output_dir:
            return
        if not dest:
            return
        fname = os.path.splitext(os.path.basename(dest))[0]
        if "csv" in self.opts and self.opts.csv:
            csv_file = os.path.join(output_dir, "{}_{}{}.csv".format(fname, pid, suffix))
            results = frames_to_csv(results)

            with open(csv_file, "w") as fp:
                csv_writer = csv.writer(fp, delimiter=",")
                for row in results:
                    csv_writer.writerow(row)

        else:
            json_file = os.path.join(output_dir, "{}_{}{}.json".format(fname, pid, suffix))
            with open(json_file, 'w') as jf:
                json.dump(results, jf, indent=self.indent)

    # -- try to parse json body and return its json attr, if possible
    def getResponse(self,body, attr):
        try:
            r = json.loads(body)
            return r[attr]
        except Exception:
            return "?"
