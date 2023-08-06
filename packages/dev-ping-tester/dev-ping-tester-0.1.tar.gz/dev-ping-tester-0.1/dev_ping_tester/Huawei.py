import re

from dev_ping_tester.BaseDevice import BaseDevice


class Huawei(BaseDevice):

    def __init__(self,name,hostname,port,username,password,protocol,debug=False):
        super(Huawei,self).__init__(name=name,hostname=hostname,port=port,username=username,password=password,protocol=protocol,enable=None,debug=debug)
        self.handler = None
        self._connect()


    def _terminal_length_zero(self):
        self.sendline("screen-length 0 temporary")

    def _run_commands(self,commands):
        resp=[]
        for command in commands:
            self.handler.send("{}\n##\n".format(command))
            self.expect(r"[>|#|$]\s?##")
            resp.append(str(self.handler.before))
            self.expect("marker.")
            # print(self.handler.after)
        return resp

    def ping(self,dest,count):
        command = "ping -c {} {}".format(count,dest)
        self.handler.send("{}\n##\n".format(command))
        self.expect(r"[>|#|$]\s?##",timeout=30)
        output = str(self.handler.before)
        packet_loss=""
        min =avg =max = 0
        for line in output.split('\n'):
            result = re.search(r"\s*([0-9]+\.[0-9]+)%\spacket\sloss",line)
            if result:
                packet_loss = float(result.group(1))
            result = re.search(r"\s*round\-trip\smin/avg/max\s=\s([0-9]+)/([0-9]+)/([0-9]+)\sms",line)
            if result:
                min = result.group(1)
                avg = result.group(2)
                max = result.group(3)
        return packet_loss,min,avg,max




    # async def _async_run_commands(self,commands):
    #     resp=[]
    #     for command in commands:
    #         self.handler.send("{}\n##\n".format(command))
    #         await self.async_expect(r"[>#\$]\s?##")
    #         resp.append(str(self.handler.before,encoding="utf-8"))
    #         await self.async_expect("marker.")
    #         # print(self.handler.after)
    #     return resp
    #
    #
    # def _configure(self,func,commands):
    #     self.handler.send("{}\n##\n".format("config t"))
    #     self.expect(r"config\)[>#\$]\s?##")
    #     resp = func(commands)
    #     self.handler.send("commit\nabort\n##\n")
    #     self.expect(r"[>|#|$]\s?##")
    #     self.expect("marker.")
    #     return resp
    #
    # async def _async_configure(self,func,commands):
    #     self.handler.send("{}\n##\n".format("config t"))
    #     await self.async_expect(r"config\)[>|#|$]\s?##")
    #     resp =await func(commands)
    #     self.handler.send("commit\nabort\n##\n")
    #     await self.async_expect(r"[>#\$]\s?##")
    #     await self.async_expect("marker.")
    #     return resp

