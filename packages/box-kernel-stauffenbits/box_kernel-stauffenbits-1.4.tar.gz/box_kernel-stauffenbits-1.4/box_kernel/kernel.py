from ipykernel.kernelbase import Kernel
import subprocess

class BoxKernel(Kernel):
    implementation = 'box_kernel'
    implementation_version = '1.2'
    language = 'box'
    language_version = '0.6'
    language_info = {
        'name': 'The Box Language',
        'mimetype': 'text/plain',
        'file_extension': '.box',
    }
    banner = "Box kernel - useful for drawing boxes"

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        bashCmd = ['box', code]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if not silent:
            stream_content = {'name': 'stdout', 'text': output.decode('utf-8')}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
