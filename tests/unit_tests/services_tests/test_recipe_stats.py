from uuid import uuid4

from mealie.schema.recipe.recipe import Recipe, RecipeCategory, RecipeTag, RecipeTool
from mealie.schema.recipe.recipe_ingredient import RecipeIngredient
from mealie.schema.recipe.recipe_step import RecipeStep
from mealie.services.recipe.recipe_service import compute_recipe_stats


def test_compute_recipe_stats_counts_each_collection():
    recipe = Recipe(
        name="Stats Recipe",
        recipe_ingredient=[RecipeIngredient(note="flour"), RecipeIngredient(note="sugar")],
        recipe_instructions=[RecipeStep(text="mix"), RecipeStep(text="bake"), RecipeStep(text="cool")],
        tools=[RecipeTool(id=uuid4(), name="Oven", slug="oven")],
        tags=[RecipeTag(name="dessert", slug="dessert")],
        recipe_category=[
            RecipeCategory(name="baking", slug="baking"),
            RecipeCategory(name="sweets", slug="sweets"),
        ],
    )

    stats = compute_recipe_stats(recipe)

    assert stats.ingredient_count == 2
    assert stats.instruction_count == 3
    assert stats.tool_count == 1
    assert stats.tag_count == 1
    assert stats.category_count == 2


def test_compute_recipe_stats_handles_empty_recipe():
    recipe = Recipe(name="Empty Recipe", recipe_ingredient=[], recipe_instructions=[])

    stats = compute_recipe_stats(recipe)

    assert stats.ingredient_count == 0
    assert stats.instruction_count == 0
    assert stats.tool_count == 0
    assert stats.tag_count == 0
    assert stats.category_count == 0
