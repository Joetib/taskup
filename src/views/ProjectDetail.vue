<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar start -->
      <div class="col-md-3 col-lg-2 pt-5 sticky-top">
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
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus alias aut iusto consequuntur ex eaque, neque quia delectus explicabo distinctio, nesciunt inventore a culpa labore sint temporibus ipsam omnis at?
        </div>
      </div>
      <!-- Sidebar end -->
      <div class="col-lg-8">
        <div class="container py-5">
          <h2>{{ project.name }}</h2>
        </div>
      </div>
      <div class="col-lg-2 p-1">
        <div class="container-fluid py-5">
            <div class="mb-5">
          <h4>Manager</h4>
          <div v-if="project.manager">
              <h5 class="m-0">{{ project.manager.name }}</h5>
              <small>{{ project.manager.email}}</small>
          </div>
          </div>
          <h4>Contributors</h4>
          <div
            class="card my-3"
            v-for="contributor in project.contributors"
            v-bind:key="contributor.id"
          >
            <div class="card-body">
              <h5 class="m-0">{{ contributor.name }}</h5>
              <small>{{ contributor.email }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      project: {},
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
  },
  mounted() {
    this.fetchProject(this.$route.params.id);
  },
};
</script>

<style>
</style>