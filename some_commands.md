### Generate Secret Key

```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

OR

```
import secrets
secrets.token_urlsafe(50)
```

---

docker run -d \
 --name db_blog \
 -e POSTGRES_USER=blog_user \
 -e POSTGRES_PASSWORD=local_pass_123 \
 -e POSTGRES_DB=blog_db \
 -p 5432:5432 \
 postgres:15
