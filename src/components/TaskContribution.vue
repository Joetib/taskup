<template>
  <div class="container-fluid bg-white py-3">
    <h4>Assignees</h4>
    <hr />
    <div>
      <select v-model="selected_user" list="users-list" class="form-select">
        <option  v-for="user in all_users" :key="user.id" :value="user.id">
          {{ user.name }} ({{ user.email }})
        </option>
      </select>

      <button @click="add_selected_user" class="btn mt-2 w-100 btn-primary">Add</button>
    </div>
    <p class="text-danger">{{ error_message }}</p>
    <div class="" v-for="user in users" :key="user.id">
      
      <div class="border border-top-0 border-start-0 border-end-0 p-2">
        <h6 class="m-0">{{ user.name }}</h6>
        <small>{{ user.email }}</small>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      selected_user: null,
      all_users: [],
      error_message: "",
    };
  },
  props: {
    project_id: null,
    task_id: null,
  },
  methods: {
    add_selected_user(){

        if (this.selected_user){
            axios.post(`project/${this.project_id}/task/${this.task_id}/add-contributor/`, {
                contributors: [this.selected_user]
            }).then(e => {
              if (e.data.success){
                this.fetch_task_contributors()
              } else {
                this.error_message = "Could not add Contributor";
              }
            }).catch(e => {
              this.error_message = "Could not add Contributor";
              console.log(e);
            })
        }
    },
    fetch_task_contributors() {
      axios
        .get(`project/${this.project_id}/task/${this.task_id}/contributors/`)
        .then((e) => {
          console.log(e.data);
          if (e.data.success) {
            this.users = e.data.result;
            
            this.all_users = e.data.all_users;
          } else {
            this.error_message = e.data.message;
          }
        })
        .catch((e) => {
          console.log(e);
          this.error_message = "Sorry could not load contributors";
          alert("An error occurred when fetching users");
        });
    },
  },
  mounted() {
    this.fetch_task_contributors();
  },
};
</script>

<style>
</style>