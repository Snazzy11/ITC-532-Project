# Starting the stack
- Run ```cp compose/.env.example compose/.env```
- Edit compose/.env and replace the placeholder values with proper values.
- Run ```cd compose && docker compose up -d --build --wait```

# Teardown
- Run ```docker compose down``` from the compose/ directory.