from app.core.routes import Routes
from app.api.views.student_sponsor import router as student_sponsor_router
__routes__ = Routes(routers=(student_sponsor_router,))
