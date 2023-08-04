import os
import traceback

class DefaultConfig:
    API_TITLE = "Machinaris API"
    API_VERSION = 0.1
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_REDOC_PATH = '/'
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////root/.chia/machinaris/dbs/default.db'
    SQLALCHEMY_BINDS = {
        'alerts':           'sqlite:////root/.chia/machinaris/dbs/alerts.db',
        'blockchains':      'sqlite:////root/.chia/machinaris/dbs/blockchains.db',
        'challenges':       'sqlite:////root/.chia/machinaris/dbs/challenges.db',
        'connections':      'sqlite:////root/.chia/machinaris/dbs/connections.db',
        'drives':           'sqlite:////root/.chia/machinaris/dbs/drives.db',
        'farms':            'sqlite:////root/.chia/machinaris/dbs/farms.db',
        'keys':             'sqlite:////root/.chia/machinaris/dbs/keys.db',
        'partials':         'sqlite:////root/.chia/machinaris/dbs/partials.db',
        'plotnfts':         'sqlite:////root/.chia/machinaris/dbs/plotnfts.db',
        'plottings':        'sqlite:////root/.chia/machinaris/dbs/plottings.db',
        'plots':            'sqlite:////root/.chia/machinaris/dbs/plots.db',
        'pools':            'sqlite:////root/.chia/machinaris/dbs/pools.db',
        'transfers':        'sqlite:////root/.chia/machinaris/dbs/transfers.db',
        'wallets':          'sqlite:////root/.chia/machinaris/dbs/wallets.db',
        'warnings':         'sqlite:////root/.chia/machinaris/dbs/warnings.db',
        'workers':          'sqlite:////root/.chia/machinaris/dbs/workers.db',

        'stat_plot_count':          'sqlite:////root/.chia/machinaris/dbs/stat_plot_count.db',
        'stat_plots_size':          'sqlite:////root/.chia/machinaris/dbs/stat_plots_size.db',
        'stat_total_coins':         'sqlite:////root/.chia/machinaris/dbs/stat_total_coins.db',
        'stat_netspace_size':       'sqlite:////root/.chia/machinaris/dbs/stat_netspace_size.db',
        'stat_time_to_win':         'sqlite:////root/.chia/machinaris/dbs/stat_time_to_win.db',
        'stat_effort':              'sqlite:////root/.chia/machinaris/dbs/stat_effort.db',
        'stat_plots_total_used':    'sqlite:////root/.chia/machinaris/dbs/stat_plots_total_used.db',
        'stat_plots_disk_used':     'sqlite:////root/.chia/machinaris/dbs/stat_plots_disk_used.db',
        'stat_plots_disk_free':     'sqlite:////root/.chia/machinaris/dbs/stat_plots_disk_free.db',
        'stat_plotting_total_used': 'sqlite:////root/.chia/machinaris/dbs/stat_plotting_total_used.db',
        'stat_plotting_disk_used':  'sqlite:////root/.chia/machinaris/dbs/stat_plotting_disk_used.db',
        'stat_plotting_disk_free':  'sqlite:////root/.chia/machinaris/dbs/stat_plotting_disk_free.db',
        'stat_farmed_blocks':       'sqlite:////root/.chia/machinaris/dbs/stat_farmed_blocks.db',
        'stat_wallet_balances':     'sqlite:////root/.chia/machinaris/dbs/stat_wallet_balances.db',
        'stat_total_balance':       'sqlite:////root/.chia/machinaris/dbs/stat_total_balance.db',
        'stat_container_mem_gib':   'sqlite:////root/.chia/machinaris/dbs/stat_container_mem_gib.db',
        'stat_host_mem_pct':        'sqlite:////root/.chia/machinaris/dbs/stat_host_mem_pct.db',
    }
    SQLALCHEMY_ECHO = True if 'FLASK_DEBUG' in os.environ and os.environ['FLASK_DEBUG'] == "development" else False
    ETAG_DISABLED = True # https://flask-smorest.readthedocs.io/en/latest/etag.html
    CONTROLLER_SCHEME = 'http'
    CONTROLLER_HOST = os.environ['controller_host'] if 'controller_host' in os.environ else 'localhost'
    CONTROLLER_PORT = os.environ['controller_api_port'] if 'controller_api_port' in os.environ else '8927'
    WORKER_SCHEME = 'http'
    WORKER_PORT = os.environ['worker_api_port'] if 'worker_api_port' in os.environ else '8927'

    STATUS_EVERY_X_MINUTES = 2  # Run status collection once every two minutes by default
    ALLOW_HARVESTER_CERT_LAN_DOWNLOAD = True
    SELECTED_WALLET_NUM = 1 # Default is read first wallet if multiple are prompted by `chia wallet show`
    RESTART_FARMER_IF_CONTAINER_MEMORY_EXCEEDS_GB = -1 # Default is to allow a fullnode unlimited memory

    BABEL_TRANSLATION_DIRECTORIES = "api/translations"
    LANGUAGES = ['en', 'de_DE', 'fr_FR', 'it_IT', 'nl_NL', 'pt_PT', 'zh']

    # For latest APScheduler library, pass the TZ through
    try:
        SCHEDULER_TIMEZONE = os.environ['TZ']
    except:
        print("Found no TZ environment variable containing timezone.  Generate a working Machinaris launch at https://www.machinaris.app")
        traceback.print_exc()
