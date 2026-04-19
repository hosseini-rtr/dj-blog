project/
├── core/
│   ├── settings/
│   └── ...
├── deploy/
│   ├── local/
│   │   └── docker-compose.yml
│   ├── production/
│   │   ├── systemd/
│   │   │   ├── blog.service
│   │   │   └── celery.service
│   │   ├── nginx/
│   │   │   └── blog.conf
│   │   └── gunicorn_config.py
│   └── scripts/
│       ├── setup_local.sh
│       └── deploy_production.sh
├── manage.py
└── requirements.txt

