# hmm, this is tricky: needs to be in an installed app :/

# class GetModelFieldsTests(TestCase):

#     def test_extracts_fields(self):
#         class TestModel(models.Model):
#             foo = models.CharField(max_length=1)
#             bar = models.CharField(max_length=1)
#             bish = models.CharField(max_length=1)
#         self.assertEqual(
#             models_utils.get_model_fields(TestModel),
#             ["foo", "bar", "bish"]
#         )
