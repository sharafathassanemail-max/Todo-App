import streamlit as st
import requests
import time
API_URL = "http://117.0.0.1:8000/api/"

#page configuration

st.set_page_config(
    page_title="WDP Tool",
    page_icon="📊",
    layout="wide"
)

st.title("Todo App")

with st.sidebar:
    st.header("Add New Task")
    new_task=st.text_input("Task Title",placeholder="Type Your Task Here")

    col1, col2 = st.columns(2)
    with col1:
        add_button = st.button("Add Task", use_container_width=True)
    with col2:
        refresh_button = st.button("Refresh", use_container_width=True)


if add_button and new_task:
    response = requests.post(
        f"{API_URL}todo.create/",
        json={'title':new_task}
    )

    if response.status_code == 200:
        st.success(f"Task added Successfully: {new_task}")
        time.sleep(1)
        st.rerun()
    else:
        st.error("Failled To Add Task")

#main contact area

col1, col2 = st.columns([3,1])
with col1:
    st.subheader("Your Tasks:")
    # fetching todos from the API
    try:
        response = requests.get(f"{API_URL}todos/")

        if response.status_code==200:
            data = response.json()
            todos = data.get("todos",[])

            if not todos:
                st.info("No Task is Add Yet")
            else:
                #displaying todos
                for todo in todos:
                    with st.container():
                        col_check,col_title,col_date,col_delete = st.columns(4)

                        #check boxes for complection of todo
                        with col_check:
                            completed=st.checkbox("",value=todo["completed"],key=f"check_{todo['id']}")

with col2:
    st.subheader("Statistics of all Tasks")

