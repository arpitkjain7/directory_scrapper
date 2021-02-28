import pandas as pd
import argparse
import os
from datetime import datetime
from web_scraper import Extract_Data, login

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--searchspec", required=True, help="search parameter")
ap.add_argument(
    "-a", "--async", required=False, help="headless mode == True, else False"
)
args = vars(ap.parse_args())
batch_id = str(int(datetime.now().timestamp() * 1000))
# driver = login(batch_id=batch_id, headless=args["async"])
# df = pd.read_csv(args["filepath"], header=None)
# user_list = df.values.tolist()
# updated_list = []
# updated_list.append(["phone number", "url", "file_path", "comments"])
# for item in user_list:
#     print(f"{item[0]=}")
out_data = Extract_Data(
    search_param=args["searchspec"], batch_id=batch_id, headless=args["async"]
)
# updated_list.append([f"+{item[0]}", item[1], file_path, comments])
print(f"{out_data=}")
df = pd.DataFrame(
    out_data, columns=["Name", "City", "State", "Contact Number", "Search parameter"]
)
# print(f"{updated_df}")
df.to_csv(os.path.join("output", f"{batch_id}.csv"), index=False, header=True)
# driver.close()
