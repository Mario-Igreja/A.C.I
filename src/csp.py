# csp.py
class CSP:
    def __init__(self):
        self.variables = []
        self.domains = {}
        self.constraints = []
    
    def add_variable(self, variable, domain):
        self.variables.append(variable)
        self.domains[variable] = domain
    
    def add_constraint(self, constraint):
        self.constraints.append(constraint)
    
    def is_solution_valid(self, assignment):
        for constraint in self.constraints:
            if not constraint(assignment):
                return False
        return True
    
    def backtrack(self, assignment={}):
        if len(assignment) == len(self.variables):
            return assignment
        
        unassigned = [v for v in self.variables if v not in assignment]
        var = unassigned[0]
        
        for value in self.domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            
            if self.is_solution_valid(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        
        return None
