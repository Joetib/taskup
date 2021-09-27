<template>
  <div id="id_11" class="container-fluid h-min-100vh">
    <div class="row h-min-100vh">
      <side-panel id="id_10"></side-panel>
      <div class="col-sm-9 col-md-9 col-lg-9 col-xl-10">
        <div class="container py-5">
            <h1 class="pb-3">Tasks</h1>

          <div class="row">
            <TaskCard
              v-for="task in tasks"
              :key="task.id"
              :task="task"
            ></TaskCard>
            <div class="col-12 py-3" v-if="!tasks.length">
              <p class="text-danger">No tasks have been assigned to you.</p>
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

<style scoped>
@media screen and (max-width: 770px) {
  #id_10{
    display: none;
  }
}
#id_11{
  min-height: 100vh;
}
</style>