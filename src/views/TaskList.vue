<template>
  <div class="container-fluid h-min-100vh">
    <div class="row h-min-100vh">
      <side-panel></side-panel>
      <div class="col-sm-9 col-md-9 col-lg-9 col-xl-10">
        <div class="container py-5">
          <div class="row">
            <div class="col-12 pt-4 pb-3">
              <h2>Tasks</h2>
            </div>

            <TaskCard
              v-for="task in tasks"
              :key="task.id"
              :task="task"
            ></TaskCard>
            <div class="col-12 py-3" v-if="!tasks.length">
              <p class="text-danger">No have been assigned to you.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SidePanel from "../components/SidePanel.vue";
import TaskCard from "../components/TaskCard.vue";
import axios from "axios";
export default {
  components: {
    TaskCard,
    SidePanel,
  },
  data() {
    return {
      error_message: "",
      tasks: [],
    };
  },
  mounted() {
    this.fetch_tasks();
  },
  methods: {
    fetch_tasks() {
      axios
        .get("/task/")
        .then((e) => {
          if (e.data.success) {
            this.tasks = e.data.result;
          } else {
            this.error_message = e.data.message;
          }
        })
        .catch((e) => {
          console.log(e);
          this.error_message = "Could not load tasks.";
        });
    },
  },
};
</script>

<style>
</style>