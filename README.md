# Flask Service Template

This is service template with flask.
It is based on Layer Architecture.
Detailed architecture structure is shown below.

```
^
├ domain (based on SQLAlchemy[1])
├ usecases
├ presentation
├ infra [2]
Dependency Flow [3]
```

[1]: ORM is a detail, but used in the model to speed up development. (We do NOT query with session in domain class.)     

[2]: Infra layer includes repository.

[3]: Dependency flow must be kept. Domain shouldn't know details like usecases, presentation, infra layer.
