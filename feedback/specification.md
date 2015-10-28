Project Spec Feedback
=====================

### Product Backlog (10/10)

### Data Models (10/10)
 * -0, Your Person model should have a OneToOneField to User rather than ForeignKey. ForeignKey is not an appropriate field for reviews on Food/Equipment/Recipe since it's OneToMany instead of ManyToOne. Same with photos. I don't understand your CookingTime model, should it be related to Recipe model instead?

### Wireframes or Mock-ups (7/10)
 * -3, You didn't include login/register/profile pages. It's also not clear how user adds a recipe.

---

### Total Score (27/30)

---

Graded by: Shuai Shao (shuaisha@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/Team153/blob/master/feedback/specification.md
