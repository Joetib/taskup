<template>
  <div id="id_11" class="container-fluid h-min-100vh">
    <div class="row h-min-100vh">
      <side-panel id="id_10" ></side-panel>
      <div class="col-sm-9 col-md-9 col-lg-9 col-xl-10">
        <div class="container-fluid position-relative">
          <div class="container">
            <h1 class="pb-3">Projects</h1>
            <div id="id_5">
            <a class="btn btn-primary btn-lg" @click="enable_create_project"
                ><i class="fa fa-plus pe-2"></i>Create Project
            </a>
            </div><hr>
            <div class="row py-4">
              <ProjectCard
                v-for="project in projects"
                :key="project.id"
                :project="project"
              />
              <div class="col-12 py-3" v-if="!projects.length">
              <p class="text-danger">No projects available at the moment.</p>
            </div>
            </div>
          </div>
          <div
            class="full-screen-form-overlay"
            v-if="open_create_project_dialog"
          >
            <CreateProject @create_project_done="create_project_done" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateProject from "../components/CreateProject.vue";
import ProjectCard from "../components/ProjectCard.vue";
import SidePanel from "../components/SidePanel.vue";

export default {
  components: {
    CreateProject,
    ProjectCard,
     SidePanel,
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
      this.$store.commit("setIsLoading", true);
      axios
        .get("/project/")
        .then((e) => {
          if (e.data.success) {
            this.projects = e.data.result.all;
          } else {
            alert("Sorry there was an error fetching projects");
          }
          this.$store.commit("setIsLoading", false);
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("setIsLoading", false);
          alert("Sorry there was an error fetching projects");
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

#id_5{
  font-weight: bold;
  position: relative;
  margin: auto;
  margin-top: 50px;
  width: 35%;
}

@media screen and (max-width: 770px) {
  #id_10{
    display: none;
  }
  #id_5{
    /* margin: 50px 0% 20px 20%; */
    width: 80%;
  }
}

#id_11{
  min-height: 100vh;
}

/* #id_12:empty:before{
  content:attr(data-placeholder);
  color:red;
} */

</style>