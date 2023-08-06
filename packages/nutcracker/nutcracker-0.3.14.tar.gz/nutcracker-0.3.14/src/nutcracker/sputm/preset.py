from nutcracker.kernel import settings, preset

from .schema import SCHEMA

sputm = preset.shell(align=1, size_fix=settings.INCLUSIVE, schema=SCHEMA)
