<template>
  <div class="container-fluid position-relative">
    <div class="row position-relative">
        <!-- Sidebar start -->
      <div class="col-md-3 col-lg-2 sticky-top">
        <div class="container">
          <ul class="list-unstyled">
            <li class="py-2">
              <a class="nav-link d-flex align-items-center gap-2" href="#">
                <i class="fa fa-file"></i> Dashboard
              </a>
            </li>
            <li class="py-2">
              <a class="nav-link d-flex align-items-center gap-2" href="#">
                <i class="fa fa-comment-alt"></i> Chats
              </a>
            </li>
          </ul>
        </div>
      </div>
      <!-- Sidebar end -->

      <div class="col-md-9 col-lg-10 py-5">
        <div class="container">
          <h2 class="mb-2">Welcome to your dashboard</h2>
          <p class="mb-5">Here you will find projects you have created and contribute to.</p>
          
          <div class="d-flex justify-content-center align-items-center">
            <a class="btn btn-primary btn-lg" @click="enable_create_project"
              ><i class="fa fa-plus pe-2"></i>Create Project</a
            >
          </div>
          <div class="row py-4">
              <div class="col-12">
                  <h2>Projects</h2>
              </div>
            <ProjectCard
              v-for="project in projects"
              :key="project.id"
              :project="project"
            />
          </div>
          
        </div>
      </div>
    </div>
    <div class="full-screen-form-overlay" v-if="open_create_project_dialog">
      <CreateProject @create_project_done="create_project_done" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateProject from "../components/CreateProject.vue";
import ProjectCard from "../components/ProjectCard.vue";

export default {
  components: {
    CreateProject,
    ProjectCard,
  },
  data() {
    return {
      open_create_project_dialog: false,
      projects: [],
    };
  },
  methods: {
    enable_create_project() {
      this.open_create_project_dialog = !this.open_create_project_dialog;
    },
    fetchProjects() {
      axios.get("/project/").then((e) => {
        if (e.data.success) {
          this.projects = e.data.result.all;
        } else {
          alert("Sorry there was an error fetching projects");
        }
      });
    },
    create_project_done(isSuccessful) {
      this.enable_create_project();
      if (isSuccessful) {
        this.fetchProjects();
      }
    },
  },
  mounted: function () {
    this.fetchProjects();
  },
};
</script>

<style>
.nav-link {
  color: #444;
}
.full-screen-form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 3;

  height: 100vh;
  width: 100vw;
}
.h-100vh {
  height: 100vh;
}
</style>