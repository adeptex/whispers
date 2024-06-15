use Mix.Config

config :app, app.Endpoint,
  secret_key_base: "aGFyZGNvZGVkVG9rZW4xMjM0Cg+/aGFyZGNvZGVkVG9rZW4xMjM0Cghardcoded01"

# Configure your database
config :app, app.Repo,
  adapter: Ecto.Adapters.Postgres,
  username: "admin",
  password: "hardcoded02",
  database: "dbname",
  pool_size: 20