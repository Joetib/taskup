<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar start -->
      <div class="col-md-3 col-lg-2 pt-5">
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
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus alias
          aut iusto consequuntur ex eaque, neque quia delectus explicabo
          distinctio, nesciunt inventore a culpa labore sint temporibus ipsam
          omnis at?
        </div>
      </div>
      <!-- Sidebar end -->
      <div class="col-lg-8">
        <div class="container py-5">
          <h2>{{ task.name }} hello</h2>
          <p>{{ task.description }}</p>
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
              v-for="task in task.tasks"
              :key="task.id"
              :task="task"
            />
          </div>
        </div>
      </div>
      <div class="col-lg-2 p-1">
        <div class="container-fluid py-5">
          <div class="mb-5">
            <h4>Manager</h4>
            <div v-if="task.project.manager">
              <h5 class="m-0">{{ task.project.manager.name }}</h5>
              <small>{{ task.project.manager.email }}</small>
            </div>
          </div>
          <h4>Contributors</h4>
          <div
            class="card my-3"
            v-for="contributor in task.project.contributors"
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
    <div class="full-screen-form-overlay" v-if="open_create_task_dialog">
      <CreateTask v-bind:project_id="project_id" @create_task_done="create_task_done" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateTask from "../components/CreateTask.vue";
import TaskCard from "../components/TaskCard.vue";

export default {
  components: {
    CreateTask,
    TaskCard,
  },
  data() {
    return {
      task: {
          
          name: "",
          project: {
              manager: {name: "name"},
          }
      },
      open_create_task_dialog: false,
    };
  },
  methods: {
    fetchTask(project_id, task_id) {
      axios.get(`/project/${project_id}/task/${task_id}/`).then((e) => {
        console.log(e.data);
        if (e.data.success) {
          this.task = e.data.result;
        } else {
          this.error = e.data.message;
        }
      });
    },
    create_task_done() {
      this.open_create_task_dialog = false;
      this.fetchTask(this.project.id)
    },
    enable_create_task() {
      this.open_create_task_dialog = true;
    },
  },
  computed: {
    project_id() {
      if (this.task.project_id !== null && this.task.project_id !== undefined) {
        return this.task.project_id;
      }
      return this.$route.params.project_id;
    },
    task_id() {
      if (this.task.id !== null && this.task.id !== undefined) {
        return this.task.id;
      }
      return this.$route.params.task_id;
    },
  },
  mounted() {
    this.fetchTask(this.project_id, this.task_id);
  },
};
</script>

<style>
</style>