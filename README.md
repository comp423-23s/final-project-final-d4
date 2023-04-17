# Computer Science Experience Labs

The Experience Labs' (XL) mission is to accelerate technical experience and build community among undergraduate CS majors at The University of North Carolina at Chapel Hill. The XL's web app, found in production at `csxl.unc.edu`, is backed by this repository.

* [Get Started with a Development Environment](docs/get_started.md)

## Sprint 0

Our sprint 0 aims to complete the story 6 of allowing users to view other users' posts. 
For the front end part, users can click the post_list tab on the left to view posts.
For the back end part, we set the post_list page to "/api/post"
For the database part, we put some inital post value in, and backend would fetch data from the database.

PS. We started on the create_post part, which corresponding to the story 4, but we have not finished that. So story 4 is not included in the sprint 0.

Our post so far include these elements:

    id: int | None = None
    title: str = ""
    description: str = ""
    content: str = ""
    created: datetime = datetime.now()
    postedBy: int | None # postedBy = userID
    comments: list['Comment'] = []     # -->(we have not implement this part in Sprint 0)
    tags: list[str] = []
    title: str = ""
    description: str = ""

## Sprint 01:
For this sprint, we continue to improve the post feature and add a comment feature. Detailed documentation is in the docs folder. After logging in to the CSXL system, users will be redirected to the project list page. They could join the post forum by creating posts, search posts, and delete posts. Users could also interact with each other by commenting the posts. 

* [Post Forum Feature](docs/post.md)
* [Comment Feature](docs/comments.md)