# -*- coding: utf-8 -*-
# extensions = ['autoapi.extension']

def run_apidoc(_):
    modules = ['api']
    for module in modules:
        cur_dir = os.path.abspath(os.path.dirname(__file__))
        output_path = os.path.join(cur_dir, module, 'doc')
        cmd_path = 'sphinx-apidoc'
        if hasattr(sys, 'real_prefix'):
            cmd_path = os.path.abspath(os.path.join( sys.prefix, 'bin', 'sphinx-apidoc'))
        subprocess.check_call([cmd_path, '-e', '-o', output_path, module, '--force'])

def setup(app):
    app.connect('builder-inited', run_apidoc)
