# Swiggy Menu Crawler

- This project fetches a restaurant's menu information from the Swiggy's API and flattens the data in a **tsv** format
- The resultant tsv file is stored in ```app/csv_data_store/``` folder
- The script also logs certain messages in the ```app/logs/``` folder
- To run the script run the following command in the root directory of the project

    ```sudo docker-compose run --rm app sh -c "python3 crawler.py <restaurant_id>"```
- Please do update the restaurant_id argument in the above command with valid int