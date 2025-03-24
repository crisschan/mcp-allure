import json
import os
from typing import Dict, List, Any

class AllureSuiteParser:
    def __init__(self, allure_report_dir: str,testcase_status=None):
        """Initialize parser with allure report directory path"""
        self.report_dir = allure_report_dir
        self.data_dir = os.path.join(allure_report_dir, 'data')
        self.suites_file = os.path.join(self.data_dir, 'suites.json')
        self.test_cases_dir = os.path.join(self.data_dir, 'test-cases')
        self.testcase_status=testcase_status
        
        if not os.path.exists(self.suites_file):
            raise FileNotFoundError(f"Suites file not found: {self.suites_file}")
    
    def parse(self) -> Dict[str, Any]:
        """Parse suites.json and test cases to return formatted data"""
        with open(self.suites_file, 'r', encoding='utf-8') as f:
            suites_data = json.load(f)
            
        result = {
            "test-suites": self._parse_suites(suites_data.get('children', []))
        }
        
        return result
    
    def _parse_suites(self, suites: List) -> List[Dict[str, Any]]:
        """Parse test suites information"""
        parsed_suites = []
        
        for suite in suites:
            # Extract suite information
            suite_info = {
                "name": suite.get('name', ''),
                # "title": suite.get('name', ''),  # Using name as title if not specified
                "description": "",  # No description in suites.json
                "status": "passed",  # Default status
                "start": "",  # Will be updated from test cases
                "stop": "",  # Will be updated from test cases
                "test-cases": []
            }
            
            # Process test cases in this suite
            if 'children' in suite:
                for child in suite['children']:
                    if 'children' in child:
                        # This is a sub-suite
                        sub_suites = self._parse_suites([child])
                        if sub_suites:
                            parsed_suites.extend(sub_suites)
                    else:
                        # This is a test case
                        test_case = self._parse_test_case(child)
                        if test_case:
                            suite_info['test-cases'].append(test_case)
                            
                            # Update suite timestamps
                            if test_case['start'] and (not suite_info['start'] or int(test_case['start']) < int(suite_info['start'])):
                                suite_info['start'] = test_case['start']
                            if test_case['stop'] and (not suite_info['stop'] or int(test_case['stop']) > int(suite_info['stop'])):
                                suite_info['stop'] = test_case['stop']
            
            if suite_info['test-cases']:
                parsed_suites.append(suite_info)
        
        return parsed_suites
    
    def _parse_test_case(self, case: Dict) -> Dict[str, Any]:
        """Parse test case information"""
        case_uid = case.get('uid', '')
        if not case_uid:
            return None
            
        case_file = os.path.join(self.test_cases_dir, f"{case_uid}.json")
        if not os.path.exists(case_file):
            return None
            
        with open(case_file, 'r', encoding='utf-8') as f:
            case_data = json.load(f)
        # Check if testcase_status is None or matches the case status

        test_case = {
            "name": case_data.get('fullName', ''),
            "title": case_data.get('title', ''),
            "description": case_data.get('description', ''),
            "severity": self._get_severity(case_data.get('labels', [])),
            "status": case_data.get('status', ''),
            "start": str(case_data.get('time', {}).get('start', '')),
            "stop": str(case_data.get('time', {}).get('stop', '')),
            "labels": case_data.get('labels', []),
            "parameters": case_data.get('parameters', []),
            "steps": self._parse_steps(case_data.get('testStage', {}).get('steps', []))
        }
        
        return test_case
    
    def _get_severity(self, labels: List) -> str:
        """Extract severity from labels"""
        for label in labels:
            if label.get('name') == 'severity':
                return label.get('value', 'normal')
        return 'normal'
    
    def _parse_steps(self, steps: List) -> List[Dict[str, Any]]:
        """Parse test steps information"""
        parsed_steps = []
        
        for step in steps:
            step_info = {
                "name": step.get('name', ''),
                "title": step.get('title', ''),
                "status": step.get('status', ''),
                "start": str(step.get('time', {}).get('start', '')),
                "stop": str(step.get('time', {}).get('stop', '')),
                "attachments": step.get('attachments', []),
                "steps": self._parse_steps(step.get('steps', []))
            }
            parsed_steps.append(step_info)
            
        return parsed_steps

def parse_allure_suite(report_dir: str) -> Dict[str, Any]:
    """Main function to parse allure suite results"""
    parser = AllureSuiteParser(report_dir)
    return parser.parse()

# def save_to_json(result,output_path: str) -> None:
#     """
#     将解析结果保存为 JSON 文件
    
#     Args:
#         output_path: 输出 JSON 文件路径
#     """
   
#     with open(output_path, 'w', encoding='utf-8') as f:
#         json.dump(result, f, ensure_ascii=False, indent=2)
#     print(f"结果已保存到: {output_path}")
# if __name__ == '__main__':
#     report_dir = '/Users/crisschan/workspace/pyspace/PyTestApiAuto/Report/html'
#     result = parse_allure_suite(report_dir)
#     save_to_json(result,'resulthtml.json')
#     print(json.dumps(result, indent=2, ensure_ascii=False))