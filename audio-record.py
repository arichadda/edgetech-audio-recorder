import time
import json
import schedule
import os

from BaseMQTTPubSub import BaseMQTTPubSub

class audioRecorder(BaseMQTTPubSub):
    def __init__(self, dataChannel=None, mqttIP=None, verbose=False):
        BaseMQTTPubSub.__init__(self)

        self.dataChannel='/aisonobouy/audio-recorder' if dataChannel==None
        self.mqttIP='mqtt' if mqttIP=None
        self.verbose = verbose
        self.flacdir="/flash/telemetry/hydrophone"
        self.hostname=os.environ["HOSTNAME"]
        self.timestamp=int(time.time())
        self.rec_time=600
        self.gain=40

        os.makedirs(self.flacdir) if not os.path.exists(self.flacdir)

        # TODO: make gain a variable
        os.popen(f'/usr/bin/amixer sset ADC {gain}db')
        
        if mqttIP:
            self.client_connection_parameters['IP'] = mqttIP
        print(f'Connecting to MQTT bus on {self.client_connection_parameters["IP"]}')
        BaseMQTTPubSub.connect_client(self)

        self.publish_to_topic('/registration',f'audio-recorder registration')

        def heartbeat(self):
            self.publish_to_topic('/heartbeat',f'audio-recorder heartbeat')

        def sendData(self, data):
            self.publish_to_topic(self.dataChannel,json.dumps(data))
            if self.verbose:
                print(f'Sent data on channel {self.dataChannel}: {json.dumps(data)}')

        def recordAudio(self):s
            self.timestamp=int(time.time())
            self.flacout=f'{self.hostname}-{self.timestamp}-hydrophone.flac'
            self.save_dest=f'{self.flacdir}/.{self.flacout}'

            bash_cmd=f'arecord -q -D sysdefault -r 44100 -d {self.rec_time} -f S16 -V mono - | ffmpeg -i - -y -ac 1 -ar 44100 -sample_fmt s16 {self.save_dest}'
            # TODO: Not sure if this is the best way to do this
            self.rec_process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            #rec_process=os.subprocess.Popen(["arecord", "-q", "-D", "sysdefault", "-r", "44100", "-d", "600", "-f", "S16", \
            #    "-V", "mono", "-", "|", "ffmpeg", "-i", "-", "-y", "-ac", "1", "-ar", "44100", "-sample_fmt", "s16", savedest])
            while rec_process != None:
                time.sleep(0.001)
            # TODO: add exceptions and notifications for record/subprocess failure
            self.sendData(self, f'saved audio file at {self.savedest}')
            return rec_process

        def stopRecordAudio(self):
            # kill sends the signal signal.SIGKILL to the process and terminate sends signal.SIGTERM
            try:
                self.rec_process.kill()
                self.sendData(self, f' audio file stopped')
            except:
                self.sendData(self, f' audio file could not be stopped')


        def main(self):
            running = True
            schedule.every(10).seconds.do(self.heartbeat)
            print('System Initialized and Running')
            while running:
                try:
                    rec_process=self.recordAudio(self)
                except KeyboardInterrupt:
                    running = False
                    print("audio-recorder application stopped!")
                except Exception as e:
                    print(e)
                except:
                    print('Unknown problem')


if __name__ == "__main__":
    audio_recorder=audioRecoder()
    audio_recorder.main()