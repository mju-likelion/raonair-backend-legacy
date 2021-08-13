module.exports = {
  apps: [{
    name: "raonair-backend",
    script: "actProjects/manage.py",
    args: "runserver",
    env_production: {
      ENV: "PROD",
      SECRET_KEY: "raonsecretkey",
      DB_HOST: "raonair-db.cdpoecd9nghs.ap-northeast-2.rds.amazonaws.com",
      DB_NAME: "raonair_db",
      DB_USER: "admin",
      DB_PASSWD: "fkdhsdpdj",
      DB_PORT: "3306",
    },
    interpreter: "/home/ubuntu/myvenv/bin/python",
  }]
}

