<template>
    <form @submit.prevent="create_task" class="form">
    
      <div class="py-4">
        <h4 class="pb-">Enter message details</h4>

      <div class="form-group py-2">
        <label for="message">Message</label>
        <textarea
          type="text"
          v-model="message"
          class="form-control form-control-lg"
        />
        
      </div>
      <div class="form-group py-3">
        <button
          type="submit"
          class="btn btn-md btn-lg btn-primary "
          
        ><i class="fa fa-plus"></i><span class="ps-3">Send</span></button>
      </div>
      </div>
    </form>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
        message: "",
      error: "",
    };
  },
  props: {
      project_id: null,
      task_id: null
  },
  methods: {
    create_task() {
      if (this.message.length > 1) {
        axios.post(`project/${this.project_id}/task/${this.task_id}/message/`, { project_id: this.project_id, task_id: this.task_id, message: this.message }).then((e) => {
          if (e.data.success) {
            this.message = "";
            this.error = "";
            this.send_close_signal(true);
          } else {
            this.error = e.data.message;
          }
        });
      }
    },
    send_close_signal(isSuccessful){
        this.$emit('create_message_done', {success: isSuccessful});
    },
  },
};
</script>

<style scoped>

</style>