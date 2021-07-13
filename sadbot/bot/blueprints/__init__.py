#    Copyright 2021 Elshan Agaev
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""All blueprints"""

from . import bp_base, bp_classes, bp_teachers, bp_exams, kbrd_blueprint

bps = [
    bp_base.bp,
    bp_classes.bp,
    bp_teachers.bp,
    bp_exams.bp,
    kbrd_blueprint.bp
]
