<template>
<div >
    <section class="section-1 container-fluid">
        <article>
            <h1 class="display-1">Project management has become easier!</h1>
            <p >
                <button id="btn-gst" class="btn btn-info" @click="$router.push('/signup')">Get Started</button>
            </p>
        </article>
            <img src="./../assets/img2.png" alt="" class="img-1 img-fluid">
    </section>

    <section>
        <div class="container text-center animate_animated animated_bounce py-5">
            <h1 class="mb-5">Our Approach</h1>
            <p>Encouraging Agile practices with a focus on <span class="fw-bold">Scrum</span> architecture</p> 
        </div>
    </section>

    <section>
        <div class="container text-center animate_animated animated_bounce py-5" >
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptas eum corporis deserunt praesentium rerum, minima cupiditate? Neque debitis, natus mollitia doloremque labore, fugiat accusantium facere sed amet sint error quo quasi autem? Nesciunt ut facilis veritatis, nulla corporis et. Quos ipsum dolorem enim tenetur vel beatae in exercitationem fugit assumenda aliquam, commodi quidem autem, aliquid libero aspernatur rem harum culpa adipisci cupiditate corrupti mollitia dolores, ab iusto porro. Laboriosam totam velit veritatis doloremque laborum natus architecto, illo nulla cupiditate aliquam sint accusamus animi, harum, fugit quis quibusdam? Deserunt vel, error necessitatibus autem suscipit delectus. Voluptatum alias ad odit ipsam saepe.
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptas eum corporis deserunt praesentium rerum, minima cupiditate? Neque debitis, natus mollitia doloremque labore, fugiat accusantium facere sed amet sint error quo quasi autem? Nesciunt ut facilis veritatis, nulla corporis et. Quos ipsum dolorem enim tenetur vel beatae in exercitationem fugit assumenda aliquam, commodi quidem autem, aliquid libero aspernatur rem harum culpa adipisci cupiditate corrupti mollitia dolores, ab iusto porro. Laboriosam totam velit veritatis doloremque laborum natus architecto, illo nulla cupiditate aliquam sint accusamus animi, harum, fugit quis quibusdam? Deserunt vel, error necessitatibus autem suscipit delectus. Voluptatum alias ad odit ipsam saepe.
        </div>
    </section>

    <section>
        <div class="container text-center animate_animated animated_bounce py-5" >
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptas eum corporis deserunt praesentium rerum, minima cupiditate? Neque debitis, natus mollitia doloremque labore, fugiat accusantium facere sed amet sint error quo quasi autem? Nesciunt ut facilis veritatis, nulla corporis et. Quos ipsum dolorem enim tenetur vel beatae in exercitationem fugit assumenda aliquam, commodi quidem autem, aliquid libero aspernatur rem harum culpa adipisci cupiditate corrupti mollitia dolores, ab iusto porro. Laboriosam totam velit veritatis doloremque laborum natus architecto, illo nulla cupiditate aliquam sint accusamus animi, harum, fugit quis quibusdam? Deserunt vel, error necessitatibus autem suscipit delectus. Voluptatum alias ad odit ipsam saepe.
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptas eum corporis deserunt praesentium rerum, minima cupiditate? Neque debitis, natus mollitia doloremque labore, fugiat accusantium facere sed amet sint error quo quasi autem? Nesciunt ut facilis veritatis, nulla corporis et. Quos ipsum dolorem enim tenetur vel beatae in exercitationem fugit assumenda aliquam, commodi quidem autem, aliquid libero aspernatur rem harum culpa adipisci cupiditate corrupti mollitia dolores, ab iusto porro. Laboriosam totam velit veritatis doloremque laborum natus architecto, illo nulla cupiditate aliquam sint accusamus animi, harum, fugit quis quibusdam? Deserunt vel, error necessitatibus autem suscipit delectus. Voluptatum alias ad odit ipsam saepe.
        </div>
    </section>
</div>
  
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Home',
  components: {
  }
}
</script>

<!--STYLING-->
<style>
.display-1{
    color:#da7f61;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: bolder;
}

.section-1{
    display: flex;
}

.section-1 article{
    padding: 5px;
    margin: 25px 5px 5px 5px;
    max-width: 50%;
    
}

@media screen and (max-width: 770px) {
    .section-1{
    display: inline-block;
}

.section-1 article{
    max-width: unset;
}
}

#btn-gst{
    position: relative;
    width: 36%;
    height: 60px;
    margin: 2em;
    margin-left: 5em;
    font-size: 1.2em;
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
}

#btn-gst:active{
    background-color: rgb(250, 203, 203);   
}

.img-1{
    width:50%;
}

@media screen and (max-width: 770px) {
    .img-1{
    width:100%;
}}

</style>
