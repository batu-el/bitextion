from pydantic import BaseModel

class Problem(BaseModel):
    description: str

class UserResponse(BaseModel):
    response: str

class ExpertQuestion(BaseModel):
    question: str

class OptimizationProblem(BaseModel):
    objective: str
    constraints: list[str]
    parameters: list[str]

class OptimizationProblemParameters(BaseModel):
    parameters: list[str]
class OptimizationProblemObjective(BaseModel):
    objective: str
class OptimizationProblemConstraints(BaseModel):
    constraints: list[str]
class SimilarityScore(BaseModel):
    similarity_score : int