#############
tw5-server
#############

TiddlySpot like server to save TiddlyWiki file online.


***********
Install
***********


.. code:: bash

   $: pip install tw5_server


***********
Usuage
***********

Let's create a wiki named tw5-test.


1. create a config file named `server.yaml`

   .. code:: yaml

      server:
        wiki_dir: wiki_dir 
      wiki:
        - name: test-wiki
          view_key: view_key
          write_key: write_key

2. create the wiki

   .. code:: bash

      ➜  demo TW5_SERVER_CONFIG=server.yaml FLASK_APP=tw5_server.flask_server flask create-wiki test-wiki
      wiki "test-wiki" is created. dir is /tmp/demo/wiki_dir/test-wiki⏎


4. run server

   .. code:: bash

      ➜  demo TW5_SERVER_CONFIG=server.yaml FLASK_APP=tw5_server.flask_server flask run
      * Serving Flask app "tw5_server.flask_server"
      * Environment: production
        WARNING: This is a development server. Do not use it in a production deployment.
        Use a production WSGI server instead.
      * Debug mode: off
      * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

5. open a browser and visit http://127.0.0.1:5000/test-wiki. Just input `test-wiki` as username, `view_key` as password at the popup basic auth window and you will see the blank wiki.

6. open wiki's `ControlPanel` and select `saving` tabbar. alter the saving method to `TiddlySpot Saver` and fill `test-wiki` as Wiki Name, `write_key` as password, `/test-wiki/store` as Server URL to the form. Then press the `Save Changes` button and the wiki will be saved to local server.
