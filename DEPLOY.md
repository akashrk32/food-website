# 🚀 Food Website Deployment Guide (Railway)

Follow this guide to deploy your **Food Website** to Railway.

## 1. Prerequisites
- [ ] **GitHub Repository**: Containing full project (backend + frontend).
- [ ] **Railway Account**: Sign up at [railway.app](https://railway.app/).
- [ ] **Railway MySQL Service**: Added to your project.
- [ ] **File Location**: Ensure `requirements.txt` and `Procfile` are in the **repository root directory** (not inside `food_backend/`).

## 2. Backend Configuration (Verified)
- **`main.py`**: Uses `MYSQLHOST`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE`, `MYSQLPORT`.
- **Creds**: No credentials are hardcoded.
- **Debug**: Debug mode is disabled.
- **`requirements.txt`**: Includes `Flask`, `flask-cors`, `mysql-connector-python`, `gunicorn`.
- **`Procfile`**: `web: gunicorn --chdir food_backend main:app`.
- **Port**: Railway automatically sets the PORT variable. Do not hardcode ports.

## 3. Initialize Cloud Database (CRITICAL)
> [!IMPORTANT]
> Without this step, the app will deploy but return empty results or table errors.

After creating your MySQL service in Railway:
1.  **Connect**: Use `MYSQL_PUBLIC_URL` or credentials to connect from **MySQL Workbench** or **DBeaver**.
2.  **Run Schema**: Execute the `schema.sql` file included in this repo.
3.  **Execute**: Run the `CREATE TABLE` and `INSERT` queries.

## 4. Deploy Backend
1.  **Source**: Deploy from your GitHub repository.
2.  **Service**: Add MySQL service inside the **same project**.
3.  **Variables**: Verify environment variables are auto-linked:
    - `MYSQLHOST`
    - `MYSQLUSER`
    - `MYSQLPASSWORD`
    - `MYSQLDATABASE`
    - `MYSQLPORT`
    
    *Railway redeploys automatically when variables change or code is pushed.*

## 5. Verify Deployment
- **Test API**: `/api/test`
- **Test Data**: `/categories` and `/recipes`

## 6. Frontend Verification
- **Static Files**: Confirm frontend HTML/CSS/JS files (like `food.html`) are committed to GitHub and **not excluded** in `.gitignore`. Otherwise, the homepage will 404.
- **Images Not Loading?**: If your uploaded images are broken, your database column implies they are truncated. Run this SQL command in your database to fix it:
    ```sql
    ALTER TABLE recipes MODIFY image_url LONGTEXT;
    ```

### Troubleshooting
- **Database error** → Check environment variables.
- **Empty data** → Check database initialization (Step 3).
- **502 / Application failed to start** → Check `Procfile`, build logs, and ensure `gunicorn` is in `requirements.txt`.
