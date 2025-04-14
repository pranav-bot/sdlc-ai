    # -------------------------------
    # Requiremnets
    # -------------------------------    


# @task
    # def consistency_check_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Review the extracted and decomposed requirements to ensure consistency and completeness. "
    #             "Identify any conflicts or missing information and provide suggestions for improvement. "
    #             "Return a JSON object with a key 'consistency_report' detailing any issues or confirming the requirements' consistency."
    #         ),
    #         expected_output="A JSON object containing a consistency report for the requirements.",
    #         agent=self.requirement_agent(),
    #         context=[self.extraction_task(), self.subtask_breakdown_task()]
    #     )

    # # -------------------------------
    # # Additional Agents and Tasks
    # # -------------------------------

    # # Documentation Agent & Task
    # @agent
    # def documentation_agent(self) -> Agent:
    #     return Agent(
    #         name="RequirementsDocumentationAgent",
    #         role="Documentation Specialist",
    #         goal=(
    #             "Transform the structured requirements data into a comprehensive, formatted requirements document that is easily understandable by both technical and non-technical stakeholders."
    #         ),
    #         backstory="You are experienced in creating detailed technical documentation from raw requirements.",
    #         description="Generates a formatted requirements document (e.g., in Markdown) from the structured JSON output.",
    #         llm="gemini/gemini-2.0-flash"
    #     )

    # @task
    # def documentation_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Using the structured requirements from the extraction and consistency check tasks, generate a comprehensive requirements document. "
    #             "Include sections for Overview, Detailed Requirements, Assumptions, and Risks. "
    #             "Return the document as a JSON object or markdown text."
    #         ),
    #         expected_output="A JSON object or markdown text representing the complete requirements document.",
    #         agent=self.documentation_agent(),
    #         context=[self.extraction_task(), self.consistency_check_task()]
    #     )

    # # Feedback Integration Agent & Task
    # @agent
    # def feedback_integration_agent(self) -> Agent:
    #     return Agent(
    #         name="FeedbackIntegrationAgent",
    #         role="Stakeholder Engagement Specialist",
    #         goal=(
    #             "Incorporate stakeholder feedback into the extracted requirements to refine and improve the development tasks. "
    #             "Merge new inputs with existing requirements and resolve conflicts."
    #         ),
    #         backstory="You are skilled in synthesizing stakeholder feedback to enhance technical requirements.",
    #         description="Integrates stakeholder feedback with the current set of requirements.",
    #         llm="gemini/gemini-2.0-flash"
    #     )

    # @task
    # def feedback_integration_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Collect and integrate stakeholder feedback provided alongside the initial requirements. "
    #             "Merge this feedback with the extracted requirements, update priorities, or add new tasks as necessary. "
    #             "Return a JSON object with a key 'updated_tasks' containing the refined list of development tasks."
    #         ),
    #         expected_output="A JSON object containing the updated development tasks after feedback integration.",
    #         agent=self.feedback_integration_agent(),
    #         context=[self.extraction_task(), self.consistency_check_task()]
    #     )

    # # Traceability Mapping Agent & Task
    # @agent
    # def traceability_mapping_agent(self) -> Agent:
    #     return Agent(
    #         name="TraceabilityMappingAgent",
    #         role="Systems Analyst",
    #         goal=(
    #             "Create a traceability matrix that links each requirement to corresponding design elements, test cases, and development tasks. "
    #             "Ensure full traceability across the SDLC."
    #         ),
    #         backstory="You excel at mapping requirements to all downstream development artifacts.",
    #         description="Generates a traceability matrix from the requirements data.",
    #         llm="gemini/gemini-2.0-flash"
    #     )

    # @task
    # def traceability_matrix_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Using the extracted requirements and subtasks, generate a traceability matrix that maps each requirement (task_id) to its corresponding design components, implementation tasks, and test cases. "
    #             "Return a JSON object with a key 'traceability_matrix' detailing these mappings."
    #         ),
    #         expected_output="A JSON object representing the traceability matrix.",
    #         agent=self.traceability_mapping_agent(),
    #         context=[self.extraction_task(), self.subtask_breakdown_task()]
    #     )

    # # Risk Analysis Agent & Task
    # @agent
    # def risk_analysis_agent(self) -> Agent:
    #     return Agent(
    #         name="RiskAnalysisAgent",
    #         role="Risk Management Specialist",
    #         goal=(
    #             "Analyze the requirements and subtasks to identify potential risks, including technical, business, and operational challenges. "
    #             "Suggest risk mitigation strategies for high-risk items."
    #         ),
    #         backstory="You are adept at evaluating risk in software projects and proposing actionable mitigations.",
    #         description="Performs risk analysis on the extracted requirements and subtasks.",
    #         llm="gemini/gemini-2.0-flash"
    #     )

    # @task
    # def risk_analysis_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Review the list of extracted requirements and their corresponding subtasks to identify any potential risks. "
    #             "For each identified risk, classify it as High, Medium, or Low and suggest potential mitigation strategies. "
    #             "Return a JSON object with a key 'risk_analysis' that includes these details."
    #         ),
    #         expected_output="A JSON object containing the risk analysis for the requirements.",
    #         agent=self.risk_analysis_agent(),
    #         context=[self.extraction_task(), self.subtask_breakdown_task()]
    #     )

    # # Change Impact Analysis Agent & Task
    # @agent
    # def change_impact_agent(self) -> Agent:
    #     return Agent(
    #         name="ChangeImpactAgent",
    #         role="Change Impact Analyst",
    #         goal=(
    #             "Assess how changes in requirements might impact other parts of the system including design, implementation, and testing. "
    #             "Provide recommendations to mitigate negative impacts of changes."
    #         ),
    #         backstory="You have a keen eye for identifying interdependencies in software projects and predicting the impact of changes.",
    #         description="Analyzes the impact of changes in requirements on related tasks and components.",
    #         llm="gemini/gemini-2.0-flash"
    #     )

    # @task
    # def change_impact_analysis_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Analyze the extracted requirements and subtasks to determine how potential changes might affect the system. "
    #             "Map each requirement to its potential impact on design, implementation, and testing. "
    #             "Return a JSON object with a key 'change_impact' detailing these mappings and recommendations."
    #         ),
    #         expected_output="A JSON object containing the change impact analysis for the requirements.",
    #         agent=self.change_impact_agent(),
    #         context=[self.extraction_task(), self.subtask_breakdown_task()]
    #     )








    # -------------------------------
    # Architecture
    # -------------------------------    






    # @task
    # def code_skeleton_task(self) -> Task:
    #     return Task(
    #         description=(
    #             f"Based on the requirement analysis, project context, tech stack, flowchart, component diagram, and structured blueprint, generate a high-level code skeleton based on the tasks: {self.tasks} that outlines the main modules, classes, functions, and interfaces. "
    #             "Return a JSON object with a key 'code_skeleton' mapping to the plain-text code skeleton."
    #         ),
    #         expected_output="A JSON object with 'code_skeleton' mapping to the high-level code skeleton.",
    #         agent=self.architecture_agent(),
    #         context=[self.flowchart_task(), self.component_diagram_task(), self.structured_components_task()]
    #     )
    
    # # -------------------------------
    # # Additional Agents and Tasks for Deep Technical Building
    # # -------------------------------

    # # Module Decomposition Agent & Task
    # @agent
    # def module_decomposition_agent(self) -> Agent:
    #     return Agent(
    #         name="ModuleDecompositionAgent",
    #         role="Module Decomposition Specialist",
    #         goal=(
    #             "Analyze the high-level code skeleton and structured components to decompose the system into discrete, logical modules. "
    #             "For each module, specify its responsibilities, functionalities, and interactions with other modules."
    #         ),
    #         backstory="You have deep expertise in decomposing complex architectures into cohesive, maintainable modules.",
    #         description="Breaks down the overall architecture into well-defined modules with clear functionalities.",
    #         llm="gemini/gemini-2.0-flash"
    #     )
    
    # @task
    # def module_decomposition_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Based on the high-level code skeleton and structured blueprint, identify and list the key modules required for the system. "
    #             "For each module, provide its name, primary functionality, responsibilities, and describe its interactions with other modules. "
    #             "Return the output as a JSON object with a key 'modules'."
    #         ),
    #         expected_output="A JSON object containing the list of modules with their functionalities and responsibilities.",
    #         agent=self.module_decomposition_agent(),
    #         context=[self.structured_components_task(), self.code_skeleton_task()]
    #     )
    
    # # Data Model Design Agent & Task
    # @agent
    # def data_model_design_agent(self) -> Agent:
    #     return Agent(
    #         name="DataModelDesignAgent",
    #         role="Data Model Architect",
    #         goal=(
    #             "Design a comprehensive data model that supports the system's functionalities. "
    #             "Identify key data entities, their relationships, attributes, and constraints."
    #         ),
    #         backstory="You are an expert in designing scalable and robust data models that underpin complex systems.",
    #         description="Generates an entity-relationship diagram (or similar representation) capturing core data entities and their relationships.",
    #         llm="gemini/gemini-2.0-flash"
    #     )
    
    # @task
    # def data_model_design_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Using the requirement analysis, project context, and output from the module decomposition task, design a detailed data model. "
    #             "Identify key entities, their attributes, relationships, and any constraints. "
    #             "Return the output as a JSON object with a key 'data_model'."
    #         ),
    #         expected_output="A JSON object representing the data model (e.g., an ERD structure).",
    #         agent=self.data_model_design_agent(),
    #         context=[self.extraction_task, self.module_decomposition_task()]
    #     )
    
    # # Interface Design Agent & Task
    # @agent
    # def interface_design_agent(self) -> Agent:
    #     return Agent(
    #         name="InterfaceDesignAgent",
    #         role="Interface Design Specialist",
    #         goal=(
    #             "Design clear and robust interfaces between the identified modules. "
    #             "Specify the API endpoints, communication protocols, and data exchange formats that facilitate module interaction."
    #         ),
    #         backstory="You excel at creating modular interfaces that ensure smooth integration between system components.",
    #         description="Creates detailed interface specifications for inter-module communication.",
    #         llm="gemini/gemini-2.0-flash"
    #     )
    
    # @task
    # def interface_design_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Based on the module decomposition and the structured blueprint, design the interfaces for each module. "
    #             "Detail the API endpoints, methods, communication protocols, and data exchange formats required for inter-module interactions. "
    #             "Return the output as a JSON object with a key 'interfaces'."
    #         ),
    #         expected_output="A JSON object representing the interface specifications between modules.",
    #         agent=self.interface_design_agent(),
    #         context=[self.module_decomposition_task(), self.structured_components_task()]
    #     )
    
    # # Security and Performance Analysis Agent & Task
    # @agent
    # def security_performance_agent(self) -> Agent:
    #     return Agent(
    #         name="SecurityPerformanceAgent",
    #         role="Security and Performance Analyst",
    #         goal=(
    #             "Evaluate the proposed architecture and module design for potential security vulnerabilities and performance bottlenecks. "
    #             "Provide actionable recommendations for risk mitigation and performance optimization."
    #         ),
    #         backstory="You are well-versed in identifying and mitigating security risks and performance issues in complex systems.",
    #         description="Performs a comprehensive security and performance analysis of the architecture and modules.",
    #         llm="gemini/gemini-2.0-flash"
    #     )
    
    # @task
    # def security_performance_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Review the entire architecture including the module decomposition and interface design. "
    #             "Identify potential security vulnerabilities and performance bottlenecks, and provide recommendations for improvements. "
    #             "Return the output as a JSON object with a key 'security_performance_analysis'."
    #         ),
    #         expected_output="A JSON object containing security and performance analysis with recommended improvements.",
    #         agent=self.security_performance_agent(),
    #         context=[self.interface_design_task(), self.code_skeleton_task()]
    #     )
    
    # # Technical Roadmap Agent & Task
    # @agent
    # def technical_roadmap_agent(self) -> Agent:
    #     return Agent(
    #         name="TechnicalRoadmapAgent",
    #         role="Technical Roadmap Planner",
    #         goal=(
    #             "Develop a detailed technical roadmap that outlines the sequence of module development, integration, testing, and deployment milestones. "
    #             "Estimate timelines and dependencies based on all prior design outputs."
    #         ),
    #         backstory="You are a seasoned technical planner capable of breaking down complex systems into actionable, time-bound roadmaps.",
    #         description="Generates a comprehensive technical roadmap detailing milestones, timelines, and dependencies for system development.",
    #         llm="gemini/gemini-2.0-flash"
    #     )
    
    # @task
    # def technical_roadmap_task(self) -> Task:
    #     return Task(
    #         description=(
    #             "Using the outputs from the code skeleton, module decomposition, data model design, interface design, and security/performance analysis, "
    #             "generate a comprehensive technical roadmap. "
    #             "The roadmap should include development milestones, estimated timelines, dependencies, and key deliverables. "
    #             "Return the output as a JSON object with a key 'technical_roadmap'."
    #         ),
    #         expected_output="A JSON object representing the technical roadmap for system development.",
    #         agent=self.technical_roadmap_agent(),
    #         context=[
    #             self.code_skeleton_task(),
    #             self.module_decomposition_task(),
    #             self.data_model_design_task(),
    #             self.interface_design_task(),
    #             self.security_performance_task()
    #         ]
    #     )
    