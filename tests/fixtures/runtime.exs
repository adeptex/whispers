use Mix.Config

config :pxblog, Pxblog.Endpoint,
  secret_key_base: "HardCodedaGFyZGNvZGVkVG9rZW4xMjM0Cg+/aGFyZGNvZGVkVG9rZW4xMjM0Cg"

# Configure your database
config :pxblog, Pxblog.Repo,
  adapter: Ecto.Adapters.Postgres,
  username: "pxblog",
  password: "h4rdc0d3dp@$$w0rd",
  database: "pxblog_prod",
  pool_size: 20