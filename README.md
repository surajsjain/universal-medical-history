## 1. Inspiration
With the advent of Machine Learning and AI, the value for data has skyrocketed in recent times and it’s projected to increase in the future. Data has become a valuable asset for several applications ranging from self-driving cars to predicting the stock market. The quality of applications depends on the richness of the dataset which is often centralized and private. 

Data related to healthcare is highly valuable as it can be used to better understand diseases, advance treatment, provide personalized care, improve diagnosis, and many more. Despite its benefits, medical data collection is challenging, and a major concern is the privacy of the patients which makes it difficult to scale.

Personal medical history is also important for the doctors when you visit them as they would have a better idea of what your body has gone through and can prescribe drugs accordingly. But today, it is usually maintained in paperwork (which makes it hard to search for something) and the hospitals that maintain digital records, confine it within themselves. We often switch places and doctors, so this makes it really hard for the new doctor at a new place to get to know about your medical history in detail.

So, our idea was to develop an application that collects medical data, give the doctors a platform to access their patients’ records and find what they want easily, and for the users to publish their basic healthcare data to be made available for use by the researchers, government agencies, policymakers, insurance corporations, and much more.

## 2. What it does

### 2 A. The Universal Medical History App is a web application that you can use for:
1. Search for doctors in your city and make an appointment at the doctor’s office.
2. Track prescriptions and upload medical test reports to a decentralized storage network, powered by Filecoin (Slate).
3. Publish the medical data on the ocean market place without compromising the privacy (keeping the contact details private), and make some money when it is purchased by researchers, insurance corporations, and others who might need healthcare records.

### 2 B. If you’re a doctor, you can do the following as well:
1. Check the appointments that you have for the day.
2. Manage all your previous and upcoming visits at one place.
3. Check your patients’ medical history (including their family history, if available).
4. Fill in the details of the patient visit.
5. Prescribe drugs, update the vaccinations provided, prescribe medical tests, and check the medical report when available.
6. Various filters are provided for you to find what you are looking for in your patients’ history.


## 3. How we built it
UMH is built out of an open-source stack, so there will be no need for paying a licensing fee to anyone when you use it. For the back end, we used Django (which is an open-source web framework for Python). For the dashboard, an open-source bootstrap-based dashboard was forked and edited to cater to the needs. The database used is Postgres, and the database for testing is an SQLite database.

Slate (by Filecoin) was accessed through their REST APIs and is used for uploading the medical test reports, as well as hosting the excel sheet data to be sold using Ocean Protocol.

When the snapshot of the data is stored on the Filecoin network, the URL generated was used to create a data asset to be sold on the Ocean Marketplace, and this process was enabled by Ocean’s library for Python (ocean.py).

We also used the Heroku cloud platform to host our Django application.

## 4. Challenges we ran into
We are relatively new to the concept of blockchains and the use of datatokens in exchange for services. So, we had to spend time understanding the theory.

## 5. Accomplishments that we're proud of
The satisfaction that our application has the potential to impact many lives is something that we are proud of the most. We believe that advancements in the field of healthcare technology will have an impact on saving lives. The fact that our application enables doctors to get critical information about patients, and support research on healthcare by making the basic medical data necessary for healthcare research available through our platform for being used by researchers who might use the data to end up solving a disease makes us proud of what we have created.

## 6. What we learned
We learned more of the theory behind blockchain technologies, the merits of decentralized applications over the traditional centralized ones, and the impact sharing data could create while maintaining privacy at the same time. We also learned about the Ocean Protocol, which we can use in other open-source projects to make the data publicly available, and using Filecoin for storing important files securely and not losing them.

## 7. What's next for Universal Medical History (UMH App)
1. Enabling compute-to-data services and adding a secret contract on top of that. 
2. Creating a decentralized medical insurance corporation that uses the medical history of the users applying for insurance in order to calculate the cost for it (Powered by DAOstack).
3. Giving a place for the users who are not able to pay the medical bills to put up a request for their bill to be paid by the OCEAN tokens generated by the monthly overall medical history data published to the OCEAN marketplace by the UMH platform.

## 8. Instructions for running
There are two ways in which you can access the UMH app:
### 8 A. Through the hosted web app on the Heroku cloud platform
Please use the following link to access the web app online: https://universalmh.herokuapp.com/
_ note: we are using the free tier of Heroku cloud for running UMH. So, it might take some time to load initially _

### 8 B. Running the Django application locally by cloning the GitHub repository:
1. Clone [UMH app's GitHub repository](https://github.com/surajsjain/universal-medical-history)
2. Create a project on [infura](https://infura.io/) and get the project ID.
3. Set up with [Slate](https://slate.host/):
    - Sign Up.
    - Get the developer API key.
    - Create a Slate.
    - Get the Slate ID.
4. Then, create a Python virtual environment, and activate it:
    - run the following command within the cloned repository `virtualenv <your_env_name>`
    - and then run `source <your_env_name>/bin/activate`
5. Export the following environment variables (note: you can change the `rinkeby` to `ropsten` or `mainnet` if you are using those chains) by running the following commands:
    - `export AQUARIUS_URL=https://aquarius.rinkeby.oceanprotocol.com`
    - `export ENV_TYPE=local_test` (if you change it to deployment, follow the **step 7**)
    - `export NETWORK_URL=https://rinkeby.infura.io/v3/<your_infura_project_id>/`
    - `export PROVIDER_URL=https://provider.rinkeby.oceanprotocol.com`
    - `export SLATE_AUTH_CODE=<your_slate_developer_api_key>`
    - `export SLATE_ID=<the_id_of_the_slate_that_you_created>`
6. Install the requirements onto your virtual environment by using `pip3 install -r requirements.txt`
7. _ (Optional) If you’ve set the ENV_TYPE as production, and you are using a Postgres database, please export the following environment variables: _
    - `export DB_HOST=<your_database_host_address>`
    - `export DB_NAME=<name_of_your_database>`
    - `export DB_PORT=<the_port_of_your_PostgreSQL_database>`
    - `export DB_USER=<database_user_name>`
    - `export DB_PASS=<password_of_the_database_user>`
8. Run the following commands to make database migrations:
    - `python3 manage.py makemigrations`
    - `python3 manage.py migrate`
9. Run the Django server on your localhost at port 8000 by using the command: `python3 manage.py runserver`
