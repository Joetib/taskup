<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar start -->
      <div class="col-md-3 col-lg-2 pt-5">
        <div class="container">
          <ul class="list-unstyled">
            <li class="py-2">
              <router-link
                class="nav-link d-flex align-items-center gap-2"
                to="/"
              >
                <i class="fa fa-home"></i> Home
              </router-link>
            </li>
            <li class="py-2">
              <router-link
                class="nav-link d-flex align-items-center gap-2"
                to="/dashboard"
              >
                <i class="fa fa-file"></i> Dashboard
              </router-link>
            </li>
          </ul>
        </div>
      </div>
      <!-- Sidebar end -->
      <div class="col-lg-7">
        <router-view />
        <div class="container py-5 d-flex justify-content-between">
          <div>
            <h2>{{ project.name }}</h2>
            <p>{{ project.description }}</p>
          </div>
          <div>
            <DeleteProjectButton
              v-bind:project_id="project_id"
            ></DeleteProjectButton>
          </div>
        </div>
        <div class="container">
          <div class="d-flex justify-content-start align-items-center">
            <a class="btn btn-primary btn-lg" @click="enable_create_task">
              <i class="fa fa-plus pe-2"></i>Create Task
            </a>
          </div>
          <div class="row py-4">
            <div class="col-12">
              <h2>Tasks</h2>
            </div>
            <TaskCard
              v-for="task in project.tasks"
              :key="task.id"
              :task="task"
            />
          </div>
        </div>
      </div>
      <div class="col-lg-3 p-0">
        <div class="container-fluid py-5">
          <ProjectContributors v-bind:project_id="project_id"></ProjectContributors>
        </div>
      </div>
    </div>
    <div class="full-screen-form-overlay" v-if="open_create_task_dialog">
      <CreateTask
        v-bind:project_id="project_id"
        @create_task_done="create_task_done"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateTask from "../components/CreateTask.vue";
import TaskCard from "../components/TaskCard.vue";
import DeleteProjectButton from "../components/DeleteProjectButton.vue";
import ProjectContributors from '../components/ProjectContributors.vue';
export default {
  components: {
    CreateTask,
    TaskCard,
    DeleteProjectButton,
    ProjectContributors,
  },
  data() {
    return {
      project: {},
      open_create_task_dialog: false,
    };
  },
  methods: {
    fetchProject(project_id) {
      axios.get(`/project/${project_id}/`).then((e) => {
        console.log(e.data);
        if (e.data.success) {
          this.project = e.data.result;
        } else {
          this.error = e.data.message;
        }
      });
    },
    create_task_done() {
      this.open_create_task_dialog = false;
      this.fetchProject(this.project.id);
    },
    enable_create_task() {
      this.open_create_task_dialog = true;
    },
  },
  computed: {
    project_id() {
      if (this.project.id !== null && this.project.id !== undefined) {
        return this.project.id;
      }
      return this.$route.params.project_id;
    },
  },
  mounted() {
    this.fetchProject(this.project_id);
  },
};
</script>

<style>
</style>