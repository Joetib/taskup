<template>
  <div id="id_11" class="container-fluid h-min-100vh">
    <div class="row h-min-100vh">
      <side-panel id="id_10"></side-panel>
      <div class="col-sm-9 col-md-9 col-lg-9 col-xl-10 px-0 px-md-2">
        <div class="row">
          <div class="col-lg-12 col-xl-8">
            <router-view />
            <div class="container py-5 d-flex justify-content-between">
              <div>
                <h2>{{ project.name }}</h2>
                <p>{{ project.description }}</p>
              </div>
              <div v-if="is_project_manager">
                <DeleteProjectButton
                  v-bind:project_id="project_id"
                ></DeleteProjectButton>
              </div>
              <!--addition of remove button-->
              <div>
                <RemoveProjectButton
                  v-bind:project_id="project_id"
                ></RemoveProjectButton>
              </div>
            </div>
            <div class="container">
              <div
                class="d-flex justify-content-start gap-2 align-items-center"
              >
                <a class="btn btn-primary btn-md" @click="enable_create_task">
                  <i class="fa fa-plus pe-2"></i>Create Task
                </a>
                <a
                  v-if="is_project_manager"
                  class="btn btn-primary btn-md me-4"
                  @click="enable_edit_project"
                >
                  <i class="fa fa-plus pe-2"></i>Edit Project
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
          <div class="col-xl-4 p-0">
            <div class="container-fluid py-5">
              <ProjectContributors
                v-bind:project_id="project_id"
                v-bind:is_project_manager="is_project_manager"
              ></ProjectContributors>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="full-screen-form-overlay" v-if="open_create_task_dialog">
      <CreateTask
        v-bind:project_id="project_id"
        @create_task_done="create_task_done"
      />
    </div>
    <div
      class="full-screen-form-overlay"
      v-if="is_project_manager && open_edit_project_dialog"
    >
      <edit-project
        v-bind:project_id="project_id"
        v-bind:project_name_prop="this.project.name"
        v-bind:project_description_prop="this.project.description"
        @edit_project_done="edit_project_done"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateTask from "../components/CreateTask.vue";
import TaskCard from "../components/TaskCard.vue";
import DeleteProjectButton from "../components/DeleteProjectButton.vue";
import ProjectContributors from "../components/ProjectContributors.vue";
import EditProject from "../components/EditProject.vue";
import SidePanel from "../components/SidePanel.vue";
export default {
  components: {
    CreateTask,
    TaskCard,
    DeleteProjectButton,
    ProjectContributors,
    SidePanel,
    EditProject,
  },
  data() {
    return {
      project: {
        name: "",
        description: "",
      },
      is_project_manager: false,
      open_create_task_dialog: false,
      open_edit_project_dialog: false,
    };
  },
  methods: {
    fetchProject(project_id) {
      this.$store.commit("setIsLoading", true);
      axios
        .get(`/project/${project_id}/`)
        .then((e) => {
          if (e.data.success) {
            this.project = e.data.result;
            this.is_project_manager = e.data.is_project_manager;
          } else {
            this.error = e.data.message;
          }
          this.$store.commit("setIsLoading", false);
        })
        .catch((e) => {
          console.log(e);
          this.error = "Sorry, could not fetch project";
          this.$store.commit("setIsLoading", false);
        });
    },
    create_task_done() {
      this.fetchProject(this.project.id);
      this.open_create_task_dialog = false;
    },
    edit_project_done() {
      this.fetchProject();
      this.open_edit_project_dialog = false;
    },
    enable_create_task() {
      this.open_create_task_dialog = true;
    },
    enable_edit_project() {
      this.open_edit_project_dialog = true;
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