import streamlit as st
import requests
import time


#static api url for smooth execution purpose 
API_URL = "http://127.0.0.1:8000/api/"

#page configuration

st.set_page_config(
    page_title="Task Todo App",
    page_icon="📝",
    layout="wide"
)

st.title("Todo App!")

with st.sidebar:

    st.header("Add New Task")
    new_task=st.text_input("Task Title",placeholder="Type your Task here")

    col1, col2 = st.columns(2)
    with col1:
        add_button = st.button("Add Task", use_container_width=True)
    with col2:
        refresh_button=st.button("Refresh", use_container_width=True)

    if add_button and new_task:
        response = requests.post(
            f"{API_URL}todos/create/",
            json={'title': new_task}
        )

        if response.status_code == 200:
            st.success(f"Task added Succesfully: {new_task}")
            time.sleep(1)
            st.rerun()

        else:
            st.error("Failed to add task")

#main content area

col1,col2 = st.columns([3,1])

with col1:
    st.subheader("You Tasks:")

    #fetching todos #we will be using Exception handling
    try:
        response=requests.get(f"{API_URL}todos/")

        if response.status_code == 200:
            data = response.json()
            todos = data.get('todos',[])

            if not todos:
                st.info("No task is added yet!")

            else:

                #displaying todos
                for todo in todos:
                    with st.container():
                        col_check,col_title,col_date,col_delete = st.columns([0.5,4,2,1])

                        #check boxes for completion of todo
                        with col_check:
                            completed=st.checkbox("",value=todo['completed'],key=f"check_{todo['id']}")

                            #updated if checkbox changed
                            if completed != todo['completed']:
                                requests.put(f"{API_URL}todos/update/{todo['id']}/",json={"completed":completed})
                                st.rerun()

                            #Task title with strikethrough if completed
                            with col_title:
                                if completed: #markdown is for purpose of content styling
                                    st.markdown(f"~~{todo['title']}~~") #~~helps to strikethrough on title
                                else:
                                    st.write(todo['title'])

                            #create date
                            with col_date:
                                st.caption(todo['created_at'])

                            # Delete button
                            with col_delete:
                                if st.button("🗑️",key=f"del_{todo['id']}"):
                                    requests.delete(f"{API_URL}todos/delete/{todo['id']}/")
                                    st.success("Deleted!")
                                    time.sleep(0.5)
                                    st.rerun()

                            st.divider()
        else:
            st.error("Cannot connect to the server. Make sure DJANGO is running at the backed!")
    except requests.exceptions.ConnectionError:
        st.error("Connection failed! Django error!")


# with col2:
#     st.subheader("Statistics of all tasks!")


#     try:
#         response = response.get(f"{API_URL}todos/")
#         if response.status_code == 200:
#             data = response.json()
#             todos = data.get('todos',[])

#             total = len(todos)

#             #display metric
#             st.metric("Total Tasks",total)
#     except:
#         pass

with col2:
    st.subheader("Statistics of all Tasks")

    try:
        response = requests.get(f"{API_URL}todos/")

        if response.status_code == 200:
            data = response.json()
            todos = data.get("todos", [])

            total_tasks = len(todos)
            completed_tasks = sum(1 for todo in todos if todo["completed"])
            pending_tasks = total_tasks - completed_tasks

            completion_rate = (
                (completed_tasks / total_tasks) * 100
                if total_tasks > 0 else 0
            )

            st.metric("Total Tasks", total_tasks)
            st.metric("Completed", completed_tasks)
            st.metric("Pending", pending_tasks)

            st.progress(completion_rate / 100)

            st.write(
                f"**Completion Rate:** {completion_rate:.1f}%"
            )

        else:
            st.error("Failed to load statistics.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to Django backend.")

