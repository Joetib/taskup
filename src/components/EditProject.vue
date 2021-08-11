<template>
  <div
    class="d-flex justify-content-center align-items-center h-100vh"
    style="background: rgba(0, 0, 0, 0.4)"
  >
    <form @submit.prevent="create_project" class="form bg-white shadow">
      <div class="d-flex flex-row justify-content-end w-100 ">
        <button @click="send_close_signal(false)" class=" btn btn-danger btn-sm rounded-0">
          <i class="fa fa-times"></i>
        </button>
      </div>
      <div class="p-md-5 p-4">
        <h4 class="pb-">Enter details to create project</h4>

      <div class="form-group py-2">
        <label for="name">Name</label>
        <input
          type="text"
          max="100"
          v-model="project_name"
          class="form-control form-control-lg"
        />

      </div>
      <div class="form-group py-2">
        <label for="description">Description</label>
        <textarea
          type="text"
        maxlength="400"
          v-model="description"
          class="form-control form-control-lg"
        />
        
      </div>
      <div class="form-group py-3">
        <button
          type="submit"
          class="btn btn-md w-100 btn-lg btn-primary "
          
        ><i class="fa fa-plus"></i><span class="ps-3">Create Project</span></button>
      </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      project_name: "",
      description: "",
      error: "",
    };
  },
  methods: {
    create_project() {
      if (this.project_name.length > 1) {
        axios.post("/project/", { name: this.project_name, description: this.description }).then((e) => {
          if (e.data.success) {
            this.projects = e.data.result.all;
            this.open_create_project_dialog = false;
            this.send_close_signal(true);
          } else {
            this.error = e.data.message;
          }
        });
      }
    },
    send_close_signal(isSuccessful){
        this.$emit('create_project_done', {success: isSuccessful});
    },
  },
};
</script>

<style scoped>
form {
  width: 50%;
  min-width: 300px;
  max-width: 500px;
}
@media screen and (max-width: 500px) {
  form {
    width: 90%;
  }
}
</style>