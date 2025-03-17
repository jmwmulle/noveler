# modules/command_handler.py

import json
import traceback
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class CommandHandler:

    def handle_commands(self, command_list):
        """
        Processes a list of command strings, aggregates their queries,
        executes them in batch via the database module, and returns aggregated results.
        """
        aggregated_results = []
        aggregated_errors = []
        for command_str in command_list:
            try:
                queries = self.parse_command_to_queries(command_str)
                for query, params in queries:
                    # Special handling for static responses
                    if query == "STATIC_API_DOC":
                        aggregated_results.append(f"API Documentation:\n{params['doc']}")
                    else:
                        result, err = run_query(query, params)
                        if err:
                            aggregated_errors.append(f"Error for '{command_str}': {err}")
                        else:
                            aggregated_results.append(f"Success for '{command_str}': {result}")
            except Exception as e:
                aggregated_errors.append(f"Exception processing '{command_str}': {traceback.format_exc()}")
        response_lines = []
        if aggregated_results:
            response_lines.append("Results:")
            response_lines.extend(aggregated_results)
        if aggregated_errors:
            response_lines.append("Errors:")
            response_lines.extend(aggregated_errors)
        return "\n".join(response_lines)

    def parse_command_to_queries(self, command_str):
        """
        Parses a command string into one or more (query, parameters) tuples.
        """
        parts = [p for p in command_str.split('/') if p]
        if not parts:
            raise ValueError("No command detected.")
        entity = parts[0].lower()
        action = parts[1].lower() if len(parts) > 1 else None
        arguments = parts[2:]
        if entity == "character":
            return self._parse_character_command(action, arguments)
        elif entity == "scenario":
            return self._parse_scenario_command(action, arguments)
        elif entity == "trait":
            return self._parse_trait_command(action, arguments)
        elif entity == "location":
            return self._parse_location_command(action, arguments)
        elif entity == "story":
            return self._parse_story_command(action, arguments)
        elif entity == "api":
            return self._parse_api_command(action, arguments)
        else:
            raise ValueError("Unsupported entity: " + entity)

    def _parse_character_command(self, action, args):
        if action == "list":
            if args and args[0].lower() != "none":
                query = "MATCH (c:BaseCharacter {id: $id}) RETURN c"
                params = {"id": args[0]}
                return [(query, params)]
            else:
                query = "MATCH (c:BaseCharacter) RETURN c.name, c.id"
                return [(query, {})]
        elif action == "create":
            if not args:
                raise ValueError("Missing JSON object for character creation.")
            data = json.loads("/".join(args))
            new_id = generate_uuid()
            query = """
            CREATE (c:BaseCharacter {id: $id})
            SET c += $data, c.created_at = timestamp()
            RETURN c
            """
            params = {"id": new_id, "data": data}
            return [(query, params)]
        else:
            raise ValueError(f"Unknown character action '{action}'")

    def _parse_scenario_command(self, action, args):
        if action == "list":
            if args and args[0].lower() != "none":
                query = "MATCH (s:Scenario {id: $id}) RETURN s"
                params = {"id": args[0]}
                return [(query, params)]
            else:
                query = "MATCH (s:Scenario) RETURN s.title, s.id"
                return [(query, {})]
        elif action == "create":
            if not args:
                raise ValueError("Missing JSON object for scenario creation.")
            data = json.loads("/".join(args))
            new_id = generate_uuid()
            query = """
            CREATE (s:Scenario {id: $id})
            SET s += $data, s.created_at = timestamp()
            RETURN s
            """
            params = {"id": new_id, "data": data}
            return [(query, params)]
        else:
            raise ValueError(f"Unknown scenario action '{action}'")

    def _parse_trait_command(self, action, args):
        if action == "list":
            query = "MATCH (t:BaseTrait) RETURN t.name, t.id"
            return [(query, {})]
        elif action == "create":
            if not args:
                raise ValueError("Missing JSON object for trait creation.")
            data = json.loads("/".join(args))
            new_id = generate_uuid()
            query = """
            CREATE (t:BaseTrait {id: $id})
            SET t += $data, t.created_at = timestamp()
            RETURN t
            """
            params = {"id": new_id, "data": data}
            return [(query, params)]
        else:
            raise ValueError(f"Unknown trait action '{action}'")

    def _parse_location_command(self, action, args):
        if action == "list":
            if args and args[0] != "None":
                query = "MATCH (l:BaseLocation {path: $path}) RETURN l.name, l.id"
                params = {"path": args[0]}
                return [(query, params)]
            else:
                query = "MATCH (l:BaseLocation) RETURN l.name, l.id"
                return [(query, {})]
        elif action == "create":
            if len(args) < 2:
                raise ValueError("Expecting a path and JSON object for location creation.")
            path = args[0]
            data = json.loads("/".join(args[1:]))
            new_id = generate_uuid()
            query = """
            CREATE (l:BaseLocation {id: $id})
            SET l += $data, l.created_at = timestamp(), l.path = $path
            RETURN l
            """
            params = {"id": new_id, "data": data, "path": path}
            return [(query, params)]
        else:
            raise ValueError(f"Unknown location action '{action}'")

    def _parse_story_command(self, action, args):
        # This implementation covers a few basic story commands.
        if action == "list":
            if args and args[0].lower() != "none":
                query = "MATCH (s:Story {id: $id}) RETURN s"
                params = {"id": args[0]}
                return [(query, params)]
            else:
                query = "MATCH (s:Story) RETURN s.title, s.id"
                return [(query, {})]
        elif action == "map":
            if args and args[0].lower() != "none":
                query = "MATCH (s:Story {id: $id}) RETURN s"
                params = {"id": args[0]}
                return [(query, params)]
            else:
                # Assume current_story_id is available as a global (or via a higher layer)
                from app import current_story_id
                query = "MATCH (s:Story {id: $id}) RETURN s"
                params = {"id": current_story_id}
                return [(query, params)]
        # For branch, prune, revise, load, we leave a NotImplemented error for now.
        else:
            raise ValueError(f"Unsupported story action: {action}")

    def _parse_api_command(self, action, args):
        api_doc = (
            "/api - Show this documentation.\n"
            "/character/list/<id or None>\n"
            "/character/create/<JSON object>\n"
            "/character/extend/<id>/<JSON object>\n"
            "/character/clone/<id>/<JSON object>\n"
            "/character/delete/<id>\n"
            "/character/update/<id>/<boolean>/<JSON object>\n"
            "/scenario/list/<id or None>\n"
            "/scenario/create/<JSON object>\n"
            "/scenario/extend/<JSON object>\n"
            "/scenario/clone/<id>/<JSON object>\n"
            "/scenario/delete/<id>\n"
            "/scenario/update/<id>/<boolean>/<JSON object>\n"
            "/scenario/link/entity/<id or location path>\n"
            "/trait/list/<id or None>\n"
            "/trait/create/<JSON object>\n"
            "/trait/extend/<id>/<JSON object>\n"
            "/trait/update/<id>/<boolean>/<JSON object>\n"
            "/trait/delete/<id>\n"
            "/location/list/<path or None>\n"
            "/location/create/<path or None>/<JSON object>\n"
            "/location/delete/<path>\n"
            "/location/update/<path>/<boolean>/<JSON object>\n"
            "/location/extend/<path>/<JSON object>\n"
            "/location/clone/<path>/<JSON object>\n"
            "/location/link/<target id/path>/<destination id/path>\n"
            "/story/list/<id or None>\n"
            "/story/map/<id or None>\n"
            "/story/prune/<message integer>/<branch id or None>\n"
            "/story/branch/<message integer>/<branch id or None>/<title>\n"
            "/story/revise/<message integer>/<new persistent prompt string>\n"
            "/story/load/<storyID>\n"
        )
        # Return a special static tuple.
        return [("STATIC_API_DOC", {"doc": api_doc})]