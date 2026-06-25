import pytest

from mealie.schema.recipe.recipe import Recipe
from mealie.schema.recipe.recipe_ingredient import RecipeIngredient
from mealie.services.recipe.recipe_service import scale_recipe


def _build_recipe() -> Recipe:
    return Recipe(
        name="Scalable Recipe",
        recipe_servings=4,
        recipe_yield_quantity=2,
        recipe_ingredient=[
            RecipeIngredient(quantity=2, note="flour"),
            RecipeIngredient(quantity=0.5, note="sugar"),
            RecipeIngredient(quantity=None, note="salt to taste"),
        ],
    )


@pytest.mark.parametrize("scale", [2, 0.5, 1, 3], ids=["double", "halve", "identity", "triple"])
def test_scale_recipe_scales_quantities_and_yield(scale: float):
    scaled = scale_recipe(_build_recipe(), scale)

    assert scaled.recipe_servings == 4 * scale
    assert scaled.recipe_yield_quantity == 2 * scale
    assert scaled.recipe_ingredient[0].quantity == 2 * scale
    assert scaled.recipe_ingredient[1].quantity == 0.5 * scale


def test_scale_recipe_preserves_null_quantities():
    """Ingredients without a quantity (e.g. "to taste") should be left untouched."""
    scaled = scale_recipe(_build_recipe(), 2)
    assert scaled.recipe_ingredient[2].quantity is None


def test_scale_recipe_does_not_mutate_the_original():
    original = _build_recipe()
    scale_recipe(original, 5)

    assert original.recipe_servings == 4
    assert original.recipe_yield_quantity == 2
    assert original.recipe_ingredient[0].quantity == 2
